# coding=utf-8

import datetime
from django.test import TestCase
from .models import Lot, User,\
    ClosedLotError, DisabledBuyoutError, BoughtoutError, LateBuyoutError, InvalidPriceError, LowPriceError,\
    PercentStepBidCalculator, FixedStepBidCalculator,\
    FixedStepBidValidator, MinimalStepBidValidator


class LotTest(TestCase):
    """Test all variants that don't use Calculator and Validator."""

    def setUp(self):
        self.lot = Lot(is_open=True, start_price=1000, start_date=datetime.datetime(2011,02,01), close_date=datetime.datetime(2011,03,01))
        self.lot.save()
        self.user = User(username="User", password="Password")
        self.user.save()

    def test_bid_on_closed_lot(self):
        self.lot.is_open = False
        self.lot.save()
        with self.assertRaises(ClosedLotError):
            self.lot.make_bid(self.user, 0)

    def test_buyout_without_buyout_price(self):
        with self.assertRaises(DisabledBuyoutError):
            self.lot.make_bid(self.user, 0, is_buyout=True)

    def test_buyout_bid_sets_correct_price(self):
        self.lot.buyout_price = 2000
        self.lot.buyout_cancel_price = 1500
        self.lot.save()
        self.lot.make_bid(self.user, is_buyout=True)
        self.assertEqual(self.lot.last_price(), 2000)

    def test_buyout_bid_closes_lot(self):
        self.lot.buyout_price = 2000
        self.lot.buyout_cancel_price = 1500
        self.lot.save()
        self.lot.make_bid(self.user, is_buyout=True)
        self.assertEqual(self.lot.is_open, False)

    def test_double_buyout(self):
        self.lot.buyout_price = 2000
        self.lot.buyout_cancel_price = 1500
        self.lot.save()
        self.lot.make_bid(self.user, 2000, is_buyout=True)
        with self.assertRaises(ClosedLotError):
            self.lot.make_bid(self.user, 2000, is_buyout=True)

    def test_double_buyout_with_trick(self):
        """Use is_open trick to simulate simultaneous buyout bids."""
        self.lot.buyout_price = 2000
        self.lot.buyout_cancel_price = 1500
        self.lot.save()
        self.lot.make_bid(self.user, 2000, is_buyout=True)
        self.lot.is_open = True
        self.lot.save()
        with self.assertRaises(BoughtoutError):
            self.lot.make_bid(self.user)


class PercentFixedLot(Lot, PercentStepBidCalculator, FixedStepBidValidator):
    pass


class PercentFixedLotTest(TestCase):

    def setUp(self):
        self.lot = PercentFixedLot(is_open=True, start_price=1000, start_date=datetime.datetime(2011,02,01), close_date=datetime.datetime(2011,03,01))
        self.lot.save()
        self.user = User(username="User", password="Password")
        self.user.save()

    def test_no_bid_last_price(self):
        self.assertEqual(self.lot.last_price(), None)

    def test_no_bid_next_price(self):
        self.assertEqual(self.lot.next_price(), self.lot.start_price)

    def test_bid_last_price(self):
        self.lot.make_bid(self.user, 1000)
        self.assertEqual(self.lot.last_price(), 1000)

    def test_bid_next_price(self):
        self.lot.make_bid(self.user, 1000)
        self.assertEqual(self.lot.next_price(), 1100)

    def test_bid_without_price(self):
        self.lot.make_bid(self.user)
        self.assertEqual(self.lot.last_price(), 1000)

    def test_two_bid_last_price(self):
        self.lot.make_bid(self.user, 1000)
        self.lot.make_bid(self.user, 1100)
        self.assertEqual(self.lot.last_price(), 1100)

    def test_three_bid_count(self):
        for _ in xrange(3):
            self.lot.make_bid(self.user)
        self.assertEqual(self.lot.bid_count(), 3)

    def test_eleven_bid_last_price(self):
        for _ in xrange(11):
            self.lot.make_bid(self.user)
        self.assertEqual(self.lot.last_price(), 2000)

    def test_twelve_bid_last_price(self):
        for _ in xrange(12):
            self.lot.make_bid(self.user)
        self.assertEqual(self.lot.last_price(), 2200)

    def test_too_big_bid(self):
        with self.assertRaises(InvalidPriceError) as e:
            self.lot.make_bid(self.user, 1200)
        self.assertEqual(e.exception.valid_next_price, 1000)

    def test_late_buyout(self):
        self.lot.buyout_price = 1100
        self.lot.save()
        self.lot.make_bid(self.user, 1000)
        self.lot.make_bid(self.user, 1100)
        with self.assertRaises(LateBuyoutError):
            self.lot.make_bid(self.user, is_buyout=True)

    def test_buyout_cancel_price(self):
        self.lot.buyout_price = 1200
        self.lot.buyout_cancel_price = 1100
        self.lot.save()
        self.lot.make_bid(self.user, 1000)
        self.lot.make_bid(self.user, 1100)
        with self.assertRaises(LateBuyoutError):
            self.lot.make_bid(self.user, is_buyout=True)

    def test_bid_before_lot_closing_increases_close_time(self):
        close_date = datetime.datetime.now() + datetime.timedelta(minutes=1)
        self.lot.close_date = close_date
        self.lot.save()
        self.lot.make_bid(self.user)
        self.assertGreater(self.lot.close_date, close_date)

    def test_bid_after_close_time_fails(self):
        close_date = datetime.datetime.now() - datetime.timedelta(minutes=1)
        self.lot.close_date = close_date
        self.lot.save()
        with self.assertRaises(ClosedLotError):
            self.lot.make_bid(self.user)

    def test_bid_after_close_time_closes_lot(self):
        close_date = datetime.datetime.now() - datetime.timedelta(minutes=1)
        self.lot.close_date = close_date
        self.lot.save()
        with self.assertRaises(ClosedLotError):
            self.lot.make_bid(self.user)
        self.assertEquals(self.lot.is_open, False)


class FixedMinimalLot(Lot, FixedStepBidCalculator, MinimalStepBidValidator):
    pass


class FixedMinimalLotTest(TestCase):

    def setUp(self):
        self.lot = FixedMinimalLot(is_open=True, start_price=1000, start_date=datetime.datetime(2011,02,01), close_date=datetime.datetime(2011,03,01))
        self.lot.save()
        self.user = User(username="User", password="Password")
        self.user.save()

    def test_bid_last_minimum_price(self):
        self.lot.make_bid(self.user, 1000)
        self.assertEqual(self.lot.last_price(), 1000)

    def test_bid_last_bigger_price(self):
        self.lot.make_bid(self.user, 1200)
        self.assertEqual(self.lot.last_price(), 1200)

    def test_bid_without_price(self):
        self.lot.make_bid(self.user)
        self.assertEqual(self.lot.last_price(), 1000)

    def test_two_bid_last_price(self):
        self.lot.make_bid(self.user, 1000)
        self.lot.make_bid(self.user, 1100)
        self.assertEqual(self.lot.last_price(), 1100)

    def test_too_low_bid(self):
        with self.assertRaises(LowPriceError) as e:
            self.lot.make_bid(self.user, 950)
        self.assertEqual(e.exception.valid_next_price, 1000)
