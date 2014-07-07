# coding=utf-8
import datetime
from decimal import Decimal, ROUND_FLOOR

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from picassoft.utils.classutils import cached_property


class LotError(Exception):

    def __init__(self, lot):
        self.lot = lot

    def __unicode__(self):
        return _(u"Lot {} exception").format(self.lot)

    def __str__(self):
        return unicode(self).encode('utf-8')


class BidError(LotError):

    def __unicode__(self):
        return _(u"Bid of lot {} is invalid").format(self.lot)


class ClosedLotError(BidError):

    def __unicode__(self):
        return _(u"Lot {} is closed, therefore bids are not allowed").format(self.lot)


class BoughtoutError(ClosedLotError):

    def __unicode__(self):
        return _(u"Lot {} is already bought out, therefore bids are not allowed anymore").format(self.lot)


class LateBuyoutError(BidError):

    def __unicode__(self):
        return _(u"Lot {} has exceeded buyout price, therefore buyouts are not allowed anymore").format(self.lot)


class DisabledBuyoutError(BidError):

    def __unicode__(self):
        return _(u"Lot {} doesn't have buyout price, therefore buyouts are not allowed").format(self.lot)


class InvalidPriceError(BidError):

    def __init__(self, lot, last_price, next_price, valid_next_price):
        self.last_price = last_price
        self.next_price = next_price
        self.valid_next_price = valid_next_price
        super(InvalidPriceError, self).__init__(lot)

    def __unicode__(self):
        return _(u"Lot {} got invalid price {} (last price was {}), must be exactly {})").format(
            self.lot, self.next_price, self.last_price, self.valid_next_price)


class LowPriceError(InvalidPriceError):

    def __unicode__(self):
        return _(u"Lot {} got invalid price {} (last price was {}), must be {} or bigger").format(
            self.lot, self.next_price, self.last_price, self.valid_next_price)


class StepBidCalculator(object):

    def next_bid(self, current_price):
        """Calculate next bid price."""
        if current_price is None:
            return self.start_price
        else:
            return current_price + self.bid_step(current_price)


class PercentStepBidCalculator(StepBidCalculator):
    price_min_delta = Decimal(100) # minimum price delta
    price_delta_percent = Decimal(10) # price delta percent
    price_precision = 2 # 2 means round to hundreds

    def bid_step(self, current_price):
        """Calculate next bid step."""
        quantize_precision = Decimal(1).scaleb(self.price_precision) # i.e Decimal("1E+2")
        delta = (current_price * self.price_delta_percent / Decimal(100)).quantize(quantize_precision, ROUND_FLOOR)
        return max(self.price_min_delta, delta)


class FixedStepBidCalculator(StepBidCalculator):
    price_delta = Decimal(100)

    def bid_step(self, current_price):
        """Calculate next bid step."""
        return self.price_delta


class FixedStepBidValidator(object):

    def validate_bid(self, current_price, next_price):
        """Validate next bid.

        Note! Self should also inherit BidCalculator"""
        valid_next_price = self.next_bid(current_price)
        if next_price != valid_next_price:
            raise InvalidPriceError(self, current_price, next_price, valid_next_price)


class MinimalStepBidValidator(object):

    def validate_bid(self, current_price, next_price):
        """Validate next bid.

        Note! Self should also inherit BidCalculator"""
        valid_next_price = self.next_bid(current_price)
        if next_price < valid_next_price:
            raise LowPriceError(self, current_price, next_price, valid_next_price)


class Lot(models.Model):
    is_open = models.BooleanField(_("Open"), default=True)
    can_bid = models.BooleanField(_("Can Bid"), default=False)

    start_price = models.DecimalField(_("Starting Price"), max_digits=17, decimal_places=2)
    buyout_price = models.DecimalField(_("Buyout Price"), max_digits=17, decimal_places=2, blank=True, null=True)
    buyout_cancel_price = models.DecimalField(_("Buyout Cancel Price"), max_digits=17, decimal_places=2, blank=True, null=True)
    estimate_price_start = models.DecimalField(_("Estimate Price Start"), max_digits=17, decimal_places=2, blank=True, null=True)
    estimate_price_end = models.DecimalField(_("Estimate Price End"), max_digits=17, decimal_places=2, blank=True, null=True)

    start_date = models.DateTimeField(_("Starting DateTime"), blank=True, null=True)
    close_date = models.DateTimeField(_("Closing DateTime"), blank=True, null=True)

    # Number of minutes before close.
    # If a bid is made during the interval, closing date is increased by that interval.
    reset_time_minutes = 5

    def __unicode__(self):
        return u"{} - {}".format(self.pk, self.start_date)

    def last_price(self):
        try:
            return self._last_price_cache
        except AttributeError:
            self._last_price_cache = self.bid_set.all().aggregate(models.Max('price'))['price__max']
            return self._last_price_cache
    last_price.short_description = _("Last Price")

    def next_price(self):
        return self.next_bid(self.last_price())
    next_price.short_description = _("Next Price")

    def bid_count(self, **kwargs):
        bids = self.bid_set
        if kwargs:
            bids = bids.filter(**kwargs)
        else:
            bids = bids.all()
        return bids.count()
    bid_count.short_description = _("Bid Count")

    def can_buyout(self):
        return self.buyout_price is not None and self.last_price() < self.buyout_cancel_price

    def make_bid(self, user, price=None, is_buyout=False):
        """Make the bid by the user for the price.

        If the price is not set, calculate bid automatically.
        If the price is set, validate it.
        Buyout closes the lot.
        Do not check permissions, just store the user. Permissions should be the concern of a view."""
        submit_date = datetime.datetime.now()

        if submit_date > self.close_date:
            self.is_open = False
            self.save()

        if not self.is_open:
            raise ClosedLotError(self)

        if is_buyout and not self.buyout_price:
            raise DisabledBuyoutError(self)

        buyouts = self.bid_count(is_buyout=True)
        if buyouts > 0:
            raise BoughtoutError(self)

        last_price = self.last_price()
        is_approved = False
        err = None
        if is_buyout:
            if last_price >= self.buyout_cancel_price:
                raise LateBuyoutError(self)
            price = self.buyout_price
            # Close on buyout
            self.is_open = False
            self.save()
        else:
            if price is None:
                price = self.next_bid(last_price)
            else:
                try:
                    self.validate_bid(last_price, price)
                    is_approved = True
                except BidError, e:
                    err = e

        # Increase the close date if the bid is close to the close date.
        if (self.close_date - submit_date).total_seconds() <= self.reset_time_minutes*60:
            self.close_date = self.close_date + datetime.timedelta(minutes=self.reset_time_minutes)
            self.save()

        self.bid_set.create(user=user, submit_date=submit_date, price=price, is_buyout=is_buyout, is_approved=is_approved)

        # Clear last price cache
        del self.__dict__['_last_price_cache']

        if err:
            raise err


class Bid(models.Model):
    lot = models.ForeignKey(Lot, verbose_name=_("Lot"))
    user = models.ForeignKey(User, verbose_name=_("User"))

    submit_date = models.DateTimeField(_("Submit Date"), auto_now_add=True)
    price = models.DecimalField(_("Bid Price"), max_digits=17, decimal_places=2)
    is_buyout = models.BooleanField(_("Buyout"))
    is_approved = models.BooleanField(_("Approved"))

    def __unicode__(self):
        return u"{} - {}".format(self.lot, self.submit_date)
