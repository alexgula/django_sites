# coding=utf-8
import os
import re
import operator
import traceback
from decimal import Decimal
from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.db import transaction, models

from picassoft.utils.profiling import timed_iterator
from tekhnoland.catalog.models import get_price_type_dict
from ...account.models import CustomerProfile
from ..models import PriceType, Product, ProductStockUnit, ProductStockUnitPrice, Order, OrderItem, \
    clear_part_number, parse_quantity, parse_decimal, parse_datetime, parse_boolean, default_price_type
from .utils import ensure_all_keys, set_fields, update_model
from .xml_utils import find_elem_children, iter_elems
from .stats import Stats


class BaseLoader(object):
    def load(self, file_name):
        """Load data from XML file."""
        pass


class DummyLoader(BaseLoader):
    name = u"dummy"

    def load(self, file_name):
        """Load data from XML file."""
        yield Stats(self.name)


class ComplexLoader(BaseLoader):
    def load(self, file_name):
        for loader in self.get_loaders(file_name):
            for result in loader.load(file_name):
                yield result

    def get_loaders(self, file_name):
        return []


class ComplexOfferLoader(ComplexLoader):
    def get_loaders(self, file_name):
        stock_id = int(re.search(r'offers_(\d+)\.', file_name).groups()[0])
        return [OfferLoader(stock_id)]  # Price loader should be different
        #return [PriceLoader(), OfferLoader(stock_id)]


class Loader(BaseLoader):
    name = u""
    model = None
    fmap = {}
    path = []

    def __init__(self, **kwargs):
        super(Loader, self).__init__(**kwargs)
        self.load_state_supported = 'load_state' in self.model._meta.get_all_field_names()

    def format_fields(self, fields):
        return fields

    def check_fields(self, fields):
        return ensure_all_keys(fields, self.fmap)

    def update_fields(self, elem, fields, full_load):
        return False

    def get_queryset(self):
        return self.model.objects.all()

    def pre_load(self, full_load):
        if self.load_state_supported and full_load:
            self.get_queryset().update(load_state=1)

    def load(self, file_name):
        """Load data from XML file."""
        stats = Stats(self.name)

        with transaction.commit_on_success():
            elem_iterator = iter_elems(file_name, *self.path)
            root = elem_iterator.next()
            full_load = not parse_boolean(root.get(u'ТолькоИзменения', 'false'))

            self.pre_load(full_load)

            counter = 0

            for elem in elem_iterator:
                fields = find_elem_children(elem, self.fmap)

                stats['loaded'] += 1

                try:
                    fields = self.format_fields(fields)
                except ValueError:
                    stats['broken'] += 1
                    continue

                if not self.check_fields(fields):
                    stats['broken'] += 1
                    continue

                is_updated = self.update_fields(elem, fields, full_load)
                if is_updated is None:
                    stats['unchanged'] += 1
                elif is_updated:
                    stats['changed'] += 1
                else:
                    stats['created'] += 1

                counter += 1
                if counter % 100 == 0:
                    transaction.commit()

            self.post_load(stats, full_load)

        yield stats

    def post_load(self, stats, full_load):
        if self.load_state_supported and full_load:
            self.get_queryset().filter(load_state=1).delete()


class ProductLoader(Loader):
    """Load catalog products from 1C. Usually file is named import.xml"""
    name = u"products"
    model = Product
    fmap = {u"Ид": 'code', u"Артикул": 'part_number', u"Наименование": 'name'}
    path = [u"Товар"]

    fmap_perlacement = {u"Код": 'code'}

    def format_fields(self, fields):
        fields['part_number_search'] = clear_part_number(fields['part_number'])
        return super(ProductLoader, self).format_fields(fields)

    def update_fields(self, elem, fields, full_load):
        updated = None

        try:
            product = Product.objects.get(code=fields['code'])
            if set_fields(product, fields):
                updated = True
            product.load_state = 0
            product.save()
        except Product.DoesNotExist:
            Product.objects.create(**fields)
            updated = False

        return updated


class ReplacementsLoader(Loader):
    """Load catalog products from 1C. Usually file is named import.xml"""
    name = u"products' replacements"
    model = Product
    fmap = {u"ИдТовара": 'code'}
    path = [u"Замены", u"Товар"]

    fmap_replacement = {u"ИдЗамены": 'code'}

    def update_fields(self, elem, fields, full_load):
        try:
            product = Product.objects.get(code=fields['code'])
        except Product.DoesNotExist:
            return None

        replacements = set()
        updated = None

        parent = elem.find(u"Замены")
        if parent is None:
            return None

        for elem_replacement in parent:
            fields = find_elem_children(elem_replacement, self.fmap_replacement)
            replacements.add(fields['code'])

        # Delete extra
        for replacement in product.replacements.all():
            if not replacement.code in replacements:
                product.replacements.remove(replacement)
                updated = True

            replacements.discard(replacement.code)

        # Insert missing
        for replacement_code in replacements:
            try:
                replacement = Product.objects.get(code=replacement_code)
            except Product.DoesNotExist:
                continue
            product.replacements.add(replacement)
            updated = True

        if full_load:
            product.load_state = 0

        if updated or full_load:
            product.save()

        return updated

    def post_load(self, stats, full_load):
        if full_load:
            for product in self.get_queryset().annotate(rc=models.Count('replacements')).filter(rc__gt=0, load_state=1):
                product.replacements.clear()
                product.load_state = 0
                product.save()
                stats['deleted'] += 1
        self.get_queryset().filter(load_state=1).update(load_state=0)


class PriceLoader(Loader):
    """Load product prices from 1C. Usually file is named offers.xml"""
    name = u"prices"
    model = PriceType
    fmap = {u"Ид": 'code', u"Наименование": 'name', u"Валюта": 'currency', u"Курс": 'currency_rate',
            u"Кратность": 'multiplier'}
    path = [u"ТипыЦен", u"ТипЦены"]

    def format_fields(self, fields):
        fields['currency_rate'] = parse_decimal(fields['currency_rate']) / parse_decimal(fields['multiplier'])
        return super(PriceLoader, self).format_fields(fields)

    def update_fields(self, elem, fields, full_load):
        del fields['multiplier']
        try:
            price_type = PriceType.objects.get(code=fields['code'])
            price_type.load_state = 0
            price_type.save()
            return True
        except PriceType.DoesNotExist:
            PriceType.objects.create(**fields)
            return False


class OfferLoader(Loader):
    """Load product offers from 1C. Usually file is named offers.xml"""
    name = u"offers"
    model = ProductStockUnit
    fmap = {u"IDТовара": 'code', u"Количество": 'quantity', u"КоличествоРезерв": 'quantity_reserved', }
    path = [u"Предложение", u"Предложение"]

    fmap_price = {u"ИдТипаЦены": 'code', u"Единица": 'unit', u"ЦенаЗаЕдиницу": 'price', u"Валюта": 'currency'}
    prices_name = u"ЦеныВсе"

    def __init__(self, stock_id, **kwargs):
        super(OfferLoader, self).__init__(**kwargs)
        self.price_types = get_price_type_dict()
        self.stock_id = int(stock_id)

    def format_fields(self, fields):
        fields['stock'] = self.stock_id

        quantity_total = parse_quantity(fields.get('quantity', '0'))
        quantity_reserved = parse_quantity(fields.get('quantity_reserved', '0'))

        # Simetimes 1C improperly exports reserved quantity bigger than total quantity, this is quick fix
        fields['quantity_reserved'] = min(quantity_total, quantity_reserved)
        # Quantity in the file is total quantity whereas quantity in the DB is available quantity
        fields['quantity'] = quantity_total - quantity_reserved

        return super(OfferLoader, self).format_fields(fields)

    def check_fields(self, fields):
        return fields['quantity'] >= 0 and fields['quantity_reserved'] >= 0 and super(OfferLoader, self).check_fields(
            fields)

    def get_queryset(self):
        return self.model.objects.filter(stock=self.stock_id)

    def get_unit(self, product, fields):
        return self.get_queryset().get(product=product)

    def update_fields(self, elem, fields, full_load):
        code = fields.pop('code')

        try:
            product = Product.objects.get(code=code)
        except Product.DoesNotExist:
            return None

        updated = None
        try:
            unit = self.get_unit(product, fields)

            if set_fields(unit, fields):
                updated = True
            unit.load_state = 0
            unit.save()
        except ProductStockUnit.DoesNotExist:
            fields['product'] = product
            unit = ProductStockUnit.objects.create(**fields)
            updated = False

        if self.load_prices(unit, elem) and updated is None:
            updated = True

        return updated

    def load_prices(self, unit, elem):
        updated = False

        parent = elem.find(self.prices_name)
        if parent is None:
            return updated

        prices = [find_elem_children(elem_price, self.fmap_price) for elem_price in elem.find(self.prices_name)]
        prices = self.normalize_prices(prices, unit)

        return update_model(ProductStockUnitPrice, dict(stock_unit=unit), operator.attrgetter('price_type_id'), prices)

    def format_price_fields(self, fields, unit):
        fields['price_type_id'] = self.price_types[fields['code']].id
        fields['stock_unit_id'] = unit.id
        fields.setdefault('unit', u"шт.")
        fields['price'] = parse_decimal(fields['price'])
        fields.setdefault('currency', "USD")
        fields.setdefault('multiplier', 1)

        del fields['code']

        return fields

    def normalize_prices(self, prices, unit):
        """Depending on stock, normalize price_list. After normalization reorder using price type id."""
        if len(prices) == 0:
            prices = self.generate_all_prices()
        elif self.stock_id == 2:
            prices = self.normalize_prices_noncondition(prices)
        else:
            prices = self.normalize_prices_regular(prices)

        result = {}
        for price in prices:
            price_id = self.price_types[price['code']].id
            price = self.format_price_fields(price, unit)
            result[price_id] = price
        return result

    def normalize_prices_regular(self, prices):
        """Filter out not known or unwanted price types."""
        return filter(lambda price: self.price_types.has_key(price['code']), prices)

    def normalize_prices_noncondition(self, prices):
        """Fill all possible prices using noncondition price. If absent, fill all prices with zeroes."""
        uncondition_prices = filter(lambda price: price['code'] == '983d0fd3-b0da-11de-9ddb-00016c1cee4f', prices)
        return self.generate_all_prices(uncondition_prices[0] if len(uncondition_prices) > 0 else None)

    def generate_all_prices(self, target_price=None):
        """Generate copies of target price for all price types, if not set, set to 0."""
        if target_price is None:
            target_price = {'price': Decimal(0)}

        def price_with_code(code):
            """Substitute price code and return copy."""
            price = target_price.copy()
            price['code'] = code
            return price

        return [price_with_code(price_type.code) for price_type in self.price_types.itervalues()]


class PendingLoader(OfferLoader):
    """Load product pending offers from 1C. Usually file is named pending.xml"""
    name = u"offers"
    model = ProductStockUnit
    fmap = {u"ID": 'code', u"IDпартии": 'batch', u"ДатаПоступления": 'pending', u"Количество": 'quantity', }
    path = [u"Ожидаемые", u"Товар"]

    fmap_price = {u"ИдТипаЦены": 'code', u"Единица": 'unit', u"ЦенаЗаЕдиницу": 'price',
                  u"Валюта": 'currency'}
    prices_name = u"ЦеныВсе"

    def __init__(self, **kwargs):
        super(PendingLoader, self).__init__(stock_id=0, **kwargs)

    def format_fields(self, fields):
        fields['pending'] = parse_datetime(fields['pending'])
        return super(PendingLoader, self).format_fields(fields)

    def check_fields(self, fields):
        return fields['pending'] >= self.start_datetime and super(PendingLoader, self).check_fields(fields)

    def get_unit(self, product, fields):
        return self.get_queryset().get(product=product, batch=fields['batch'])

    def load(self, file_name):
        self.start_datetime = datetime.now()
        self.get_queryset().filter(pending__lt=self.start_datetime).delete()
        return super(PendingLoader, self).load(file_name)


class ClientLoader(Loader):
    """Load product prices from 1C. Usually file is named offers.xml"""
    name = u"clients"
    model = CustomerProfile
    fmap = {u"ID": 'code1c', u"Наименование": 'username1c', u"Логин": 'username', u"Почта": 'email',
            u"ТипЦен": 'price_type_id', u"Скидка": 'discount'}
    path = [u"Контрагент"]
    update_user_fields = ['email']
    update_profile_fields = ['code1c', 'username1c', 'price_type_id', 'discount']

    def __init__(self, **kwargs):
        super(ClientLoader, self).__init__(**kwargs)
        self.price_types = get_price_type_dict()
        self.default_price_type = default_price_type()

    def check_fields(self, fields):
        return ensure_all_keys(fields, self.fmap, ['email'])

    def format_fields(self, fields):
        fields['price_type_id'] = self.price_types.get(fields['price_type_id'], self.default_price_type).id
        fields['discount'] = parse_decimal(fields['discount'])

        fields['username'] = fields.get('username', None)  # Some clients don't have login

        return super(ClientLoader, self).format_fields(fields)

    def update_fields(self, elem, fields, full_load):
        username = fields.pop('username')

        if 'email' in fields and fields['email'] is not None:
            # If email is not set in 1C, do not delete it from site
            del fields['email']

        updated = None
        try:
            user = User.objects.get(username=username)
            if set_fields(user, fields, self.update_user_fields):
                user.save()
                updated = True

            profile = CustomerProfile.objects.get(user__username=username)
            if (not profile.code1c or profile.code1c == fields['code1c']) and set_fields(profile, fields,
                                                                                         self.update_profile_fields):
                profile.save()
                updated = True
        except (User.DoesNotExist, CustomerProfile.DoesNotExist):
            pass

        return updated


class OrderLoader(Loader):
    """Load product offers from 1C. Usually file is named offers.xml"""
    name = u"orders"
    model = Order
    fmap = {u"ИдЗаказаСайт": 'id', u"ИдЗаказа": 'code', u'Номер': 'number', u"Дата": 'date',
            u"ИдКлиента": 'customer', u"Логин": 'username',
            u"Статус": 'status', u"ФормаОплаты": 'payment_type', u"Валюта": 'currency', u"Курс": 'currency_rate',
            u"Сумма": 'sum', u"Комментарий": 'comment', }
    path = [u"Документы", u"Документ"]

    fmap_items = {u"ИдПозиции": 'code', u"Артикул": 'part_number', u"Название": 'name',
                  u"Склад": 'stock', u"ДатаОжидания": 'pending',
                  u"ЦенаВалюта": 'price', u"Цена": 'user_price', u"Количество": 'quantity', u"Сумма": 'sum',
                  u"ЕдиницаИзмерения": 'unit', u"Коэффициент": 'multiplier', u"Замена": 'is_replacement',
                  u"Статус": 'status', }
    items_name = u"Позиции"

    def check_fields(self, fields):
        user_criteria = dict(customerprofile__code1c=fields['customer'])
        if 'username' in fields:
            user_criteria['username'] = fields.pop('username')

        try:
            fields['customer'] = User.objects.get(**user_criteria)
        except (User.DoesNotExist, MultipleObjectsReturned):
            if 'id' in fields:
                del fields['customer']  # if old order, ignore the issue
            else:
                return False

        return ensure_all_keys(fields, self.fmap, ['id', 'date', 'customer', 'username'])

    def format_fields(self, fields):
        if 'id' in fields:
            fields['id'] = int(fields['id'])
        if 'date' in fields:
            if 'id' in fields:
                del fields['date']  # Do not load date for orders created on site
            else:
                fields['date'] = parse_datetime(fields['date'])

        fields['status'] = int(fields.get('status', '0'))
        fields['payment_type'] = int(fields['payment_type'])
        fields['currency_rate'] = parse_decimal(fields['currency_rate'])
        fields['sum'] = parse_decimal(fields.get('sum', '0'))
        return super(OrderLoader, self).format_fields(fields)

    def update_fields(self, elem, fields, full_load):
        updated = None
        order_id = fields.pop('id', None)
        if order_id is None:
            Order.objects.create(**fields)
            updated = False
        else:
            try:
                order = self.get_queryset().get(id=order_id)

                if self.load_items(order, elem):
                    updated = True

                if set_fields(order, fields):
                    order.save()
                    updated = True
            except Order.DoesNotExist:
                pass

        return updated

    def load_items(self, order, elem):
        parent = elem.find(self.items_name)
        if parent is None:
            return False

        item_fields = dict([self.format_item_fields(elem_item, order) for elem_item in elem.find(self.items_name)])

        updated = update_model(OrderItem, dict(order=order), lambda item: (item.code, item.stock),
                               item_fields)
        return updated

    def format_item_fields(self, elem, order):
        item = find_elem_children(elem, self.fmap_items)

        item['order_id'] = order.id

        item['stock'] = int(item.get('stock', '0'))

        # Sometimes we got incorrect value 3
        if not (0 <= item['stock'] <= 2):
            item['stock'] = 1

        item['pending'] = parse_datetime(item['pending'])
        item['price'] = parse_decimal(item['price'])
        item['user_price'] = parse_decimal(item['user_price'])
        item['quantity'] = parse_quantity(item['quantity'])
        item['sum'] = parse_decimal(item['sum'])
        item['multiplier'] = parse_decimal(item['multiplier'])
        item['is_replacement'] = parse_boolean(item['is_replacement'])
        item['status'] = int(item['status'])

        return (item['code'], item['stock']), item


def import_files(filedir, cleanup):
    file_types = [
        ('products', ProductLoader),
        ('replacement', ReplacementsLoader),
        ('offers_1', ComplexOfferLoader),
        ('offers_2', ComplexOfferLoader),
        ('pending', PendingLoader),
        ('clients', ClientLoader),
        ('doc', OrderLoader),
    ]

    for file_type, loader in file_types:
        result = []
        filename = '{}.xml'.format(file_type)
        fullpath = os.path.join(filedir, filename)

        if not os.path.exists(fullpath):
            continue

        yield False, filename, u""
        try:
            for elapsed, stats in timed_iterator(loader().load(fullpath)):
                for line in stats.format_with_time(elapsed):
                    result.append(line)
        except Exception:
            result.append(traceback.format_exc())
        yield True, filename, u"\n".join(result)

        if cleanup:
            os.remove(fullpath)
