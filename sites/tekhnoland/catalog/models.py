# coding=utf-8
import re
from decimal import Decimal
from collections import OrderedDict
from datetime import datetime
from django.db.models import permalink, F
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.db import models, transaction
from .model_choices import *
from .exchange.utils import set_fields

part_number_re = re.compile(u'[^\w\d]+', flags=re.UNICODE)
whitespaces = re.compile(u'\s', flags=re.UNICODE)


def clear_part_number(part_number):
    return part_number_re.sub(u'', unicode(part_number).upper())


def parse_datetime(datetime_string):
    """Try parse date and time if present or date only."""
    try:
        return datetime.strptime(datetime_string, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return datetime.strptime(datetime_string, '%Y-%m-%d')


def parse_quantity(quantity_string):
    return int(parse_decimal(quantity_string))


def parse_decimal(decimal_string):
    return Decimal(re.sub(whitespaces, '', decimal_string or '0').replace(',', '.'))


def parse_boolean(boolean_string):
    return boolean_string.lower() == u'true'


def get_price_type_dict():
    return {t.code: t for t in PriceType.objects.all()}


def default_price_type():
    return PriceType.objects.get(code='e39e8663-187b-11dd-a56f-0017319081ce') # Розничная


def get_user_price_type(user):
    if user.is_authenticated():
        price_type = user.profile.price_type
        if price_type is None:
            return default_price_type()
        return price_type
    else:
        return default_price_type()


def get_user_price(price, currency_rate):
    return price * currency_rate


def stock_items(objects, object_converter):
    for item in objects:
        yield object_converter(item)


def get_stocks(items, sort_key):
    """Build ordered dictionary of stocks, each consists of sorted object list to render."""

    # Build list of all stocks
    stocks = OrderedDict()
    for stock in STOCK_CHOICES:
        stocks[stock[0]] = {'name': stock[1], 'objects': []}

    # Fill stocks
    for stock_id, stock_object in items:
        stocks[stock_id]['objects'].append(stock_object)

    # Move pending to the end
    pending = stocks.pop(0)
    stocks[0] = pending

    # Remove empty stocks and sort non-empty stock objects by key profided
    clean_stocks = OrderedDict()
    for stock_id, stock in stocks.iteritems():
        if stock['objects']:
            stock['objects'] = sorted(stock['objects'], key=sort_key)
            clean_stocks[stock_id] = stock

    return clean_stocks


def stock_unit_can_be_ordered(item):
    # non_zero_price = item['price'] > 0
    pending = item['stock_unit__pending'] is not None
    in_stock = item['stock_unit__quantity'] > 0

    return pending or in_stock


def stock_unit_reserve(stock_unit_id, quantity):
    # Optimistic locking in case of race
    try:
        ProductStockUnit.objects.filter(id=stock_unit_id).update(
            quantity=F('quantity') - quantity,
            quantity_reserved=F('quantity_reserved') + quantity,
        )
    except IntegrityError:
        transaction.rollback()
        raise ReserveException(quantity)


class ReserveException(Exception):
    def __init__(self, quantity):
        self.quantity = quantity

    def __str__(self):
        return "Cannot reserve {} items".format(self.quantity)


class PriceType(models.Model):
    code = models.CharField(u"Код 1С", max_length=36, unique=True)
    name = models.CharField(u"Название", max_length=100)
    currency = models.CharField(u"Валюта", max_length=3, choices=CURRENCY_CHOICES)
    currency_rate = models.DecimalField(u"Курс", max_digits=16, decimal_places=4)
    load_state = models.IntegerField(u"Состояние загрузки", default=0, choices=LOAD_STATE_CHOICES,
                                     help_text=u"Служебное поле для использования во время загрузки")

    class Meta:
        ordering = ['name']
        verbose_name = u"тип цены"
        verbose_name_plural = u"типы цен"

    def __unicode__(self):
        return self.name


class Product(models.Model):
    code = models.CharField(u"Код 1С", max_length=36, unique=True)
    part_number = models.CharField(u"Артикул", max_length=25, blank=True)
    part_number_search = models.CharField(u"Артикул (поиск)", max_length=25, blank=True, db_index=True)
    name = models.CharField(u"Название", max_length=100, blank=True)
    replacements = models.ManyToManyField('self', verbose_name=u"Замены", symmetrical=False, blank=True)
    load_state = models.IntegerField(u"Состояние загрузки", default=0, choices=LOAD_STATE_CHOICES,
                                     help_text=u"Служебное поле для использования во время загрузки")

    class Meta:
        ordering = ['part_number']
        verbose_name = u"товар"
        verbose_name_plural = u"товары"

    def __unicode__(self):
        return u"{} {}".format(self.part_number, self.name)


class ProductStockUnit(models.Model):
    product = models.ForeignKey(Product, verbose_name=u"Товар")
    stock = models.PositiveIntegerField(u"Склад", choices=STOCK_CHOICES)
    batch = models.CharField(u"Код партии 1С", max_length=36, blank=True)
    pending = models.DateTimeField(u"Дата ожидания", blank=True, null=True)
    quantity = models.PositiveIntegerField(u"Количество")
    quantity_reserved = models.PositiveIntegerField(u"Количество в резерве", default=0)
    load_state = models.IntegerField(u"Состояние загрузки", default=0, choices=LOAD_STATE_CHOICES,
                                     help_text=u"Служебное поле для использования во время загрузки")

    class Meta:
        verbose_name = u"позиция"
        verbose_name_plural = u"позиции"
        unique_together = 'product', 'stock', 'batch',

    def __unicode__(self):
        return u"{} {}".format(self.product, self.stock)


class ProductStockUnitPrice(models.Model):
    price_type = models.ForeignKey(PriceType, verbose_name=u"Тип цены")
    stock_unit = models.ForeignKey(ProductStockUnit, verbose_name=u"Позиция")
    unit = models.CharField(u"Единица измерения", max_length=10)
    price = models.DecimalField(u"Цена", max_digits=16, decimal_places=4)
    currency = models.CharField(u"Валюта", max_length=3, choices=CURRENCY_CHOICES)
    multiplier = models.DecimalField(u"Коэффициент", max_digits=16, decimal_places=4)

    class Meta:
        verbose_name = u"цена"
        verbose_name_plural = u"цены"

    def __unicode__(self):
        return u"{} {} за {} {}".format(self.price, self.currency, self.multiplier, self.unit)

    def user_price(self):
        return get_user_price(self.price, self.price_type.currency_rate)


class Order(models.Model):
    code = models.CharField(u"Код 1С", max_length=36, blank=True)
    number = models.CharField(u"Номер заказа", max_length=20, blank=True)
    date = models.DateTimeField(u"Дата оформления", auto_now_add=True)
    customer = models.ForeignKey(User, verbose_name=u"Клиент")
    status = models.IntegerField(u"Статус", choices=ORDER_STATUS_CHOICES)
    payment_type = models.IntegerField(u"Форма оплаты", choices=PAYMENT_TYPE_CHOICES)
    currency = models.CharField(u"Валюта", max_length=3, choices=CURRENCY_CHOICES)
    currency_rate = models.DecimalField(u"Курс", max_digits=16, decimal_places=4)
    sum = models.DecimalField(u"Сумма", max_digits=16, decimal_places=4)
    comment = models.TextField(u"Комментарий")
    export_state = models.IntegerField(u"Состояние выгрузки", default=-1, choices=EXPORT_STATE_CHOICES,
                                       help_text=u"Служебное поле для использования во время выгрузки")

    class Meta:
        verbose_name = u"заказ"
        verbose_name_plural = u"заказы"
        ordering = ['-id', ]

    def __unicode__(self):
        return u"№{} от {} для {} на {:.2f} грн".format(self.pk, self.date.strftime('%Y-%m-%d %H:%M'),
                                                        self.customer.profile.full_name(), self.sum)

    @permalink
    def get_absolute_url(self):
        return 'catalog:order_detail', None, dict(pk=self.pk)

    def customer_full_name(self):
        return self.customer.get_full_name()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name=u"Заказ")
    code = models.CharField(u"Код 1С", max_length=36)
    part_number = models.CharField(u"Артикул", max_length=25, blank=True)
    name = models.CharField(u"Название", max_length=100, blank=True)
    stock = models.PositiveIntegerField(u"Склад", choices=STOCK_CHOICES)
    pending = models.DateTimeField(u"Дата ожидания", blank=True, null=True)
    price = models.DecimalField(u"Цена в валюте", max_digits=16, decimal_places=4)
    user_price = models.DecimalField(u"Цена в грн", max_digits=16, decimal_places=4)
    quantity = models.PositiveIntegerField(u"Количество")
    sum = models.DecimalField(u"Сумма", max_digits=16, decimal_places=4)
    unit = models.CharField(u"Единица измерения", max_length=10)
    multiplier = models.DecimalField(u"Коэффициент", max_digits=16, decimal_places=4)
    is_replacement = models.BooleanField(u"Замена")
    status = models.IntegerField(u"Статус", choices=ORDER_STATUS_CHOICES, default=0)

    class Meta:
        verbose_name = u"позиция заказа"
        verbose_name_plural = u"позиции заказа"
        unique_together = 'order', 'code', 'stock'

    def __unicode__(self):
        return u"{} {}".format(self.name, self.order)


class BasketItemManager(models.Manager):
    @staticmethod
    def prices(user):
        price_type = get_user_price_type(user)
        prices = ProductStockUnitPrice.objects.filter(price_type=price_type, stock_unit__basketitem__customer=user,
                                                      stock_unit__load_state__gte=0)
        return prices, price_type

    def stats(self, user):
        prices, price_type = self.prices(user)
        items = prices.values_list('price', 'stock_unit__basketitem__quantity')
        item_sum = sum([item[0] * item[1] * price_type.currency_rate for item in items])
        item_count = sum([item[1] for item in items])
        return item_sum, item_count

    def user_items_dict(self, user):
        items = self.filter(customer_id=user.id)
        return {item.stock_unit_id: item for item in items}

    @staticmethod
    def put(customer, stock_unit_id, quantity, is_replacement):
        """Put an item into basket.

        If given quantity is zero, delete the item.
        If try to delete an absent item and also in the case of the rare race condition raise DoesNotExist exception.
        Race condition can be triggered if try to add an item and in the same time delete it.

        Return old quantity if the item was in the basket."""
        old_quantity = None
        if quantity > 0:
            try:
                BasketItem.objects.create(stock_unit_id=stock_unit_id, customer=customer, quantity=quantity,
                                          is_replacement=is_replacement)
            except IntegrityError:
                transaction.rollback()
                item = BasketItem.objects.get(stock_unit=stock_unit_id, customer=customer)
                old_quantity = item.quantity
                if item.quantity != quantity or item.is_replacement != is_replacement:
                    item.quantity = quantity
                    item.is_replacement = is_replacement
                    item.save()
        else:
            BasketItem.objects.filter(stock_unit=stock_unit_id, customer=customer).delete()

        return old_quantity

    def update_basket(self, customer, items):
        """Update or delete items in the basket. Note that inserts are done using the other method.

        Items is the dictionary keyed by a basket item id and values are the dictionaries:
        - quantity: int
        - deleted: boolean
        - selected: boolean"""
        for basket_item in BasketItem.objects.filter(customer=customer):
            id = basket_item.id
            if not items.has_key(id) or items[id]['deleted']:
                basket_item.delete()
            elif set_fields(basket_item, items[id], ['quantity', 'selected']):
                basket_item.save()


class BasketItem(models.Model):
    stock_unit = models.ForeignKey(ProductStockUnit, verbose_name=u"Товарная позиция")
    customer = models.ForeignKey(User, verbose_name=u"Клиент")
    quantity = models.IntegerField(u"Количество")
    is_replacement = models.BooleanField(u"Замена")
    selected = models.BooleanField(u"В заказ", default=True)

    objects = BasketItemManager()

    class Meta:
        unique_together = 'stock_unit', 'customer'
