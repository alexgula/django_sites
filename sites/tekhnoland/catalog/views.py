# coding=utf-8
import logging
import operator
from collections import OrderedDict
from decimal import Decimal, InvalidOperation
from smtplib import SMTPException

from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404, HttpResponse
from django.template.context import Context
from django import http
from django.views.generic.base import View
from django.db import transaction
import six
import xlwt
from xlwt import *

from picassoft.utils.classviews import JSONResponseMixin, LoginRequiredMixin
from .forms import UploadFileForm
from .models import ProductStockUnitPrice, BasketItem, Order, OrderItem, ReserveException,\
    clear_part_number, parse_quantity, get_user_price_type, stock_items, get_stocks, get_user_price,\
    stock_unit_can_be_ordered, stock_unit_reserve
from .forms import OrderForm
from .templatetags import catalogtags
from .email import send_order_to_customer, send_order_to_admin
from .exchange.utils import map_dict
from .exchange.export import ComplexExporter, ExporterSuccess
from ..navigation.models import StaticNode
from ..navigation.views import HomeNavigationView, NavigationTemplateView,\
    NavigationFormView, NavigationCreateView, NavigationDetailView, NavigationListView
from ..exchange1c.exchange import run_exchange


logger = logging.getLogger(__name__)


class Search(NavigationTemplateView):
    template_name = 'catalog/search.html'
    trail_parent = HomeNavigationView
    trail = StaticNode(u'Поиск детали', 'catalog:search')

    def get(self, request, *args, **kwargs):
        self.part_number = self.request.GET.get('part_number', u"")
        self.request.session['part_number'] = self.part_number

        context = self.get_context_data()

        return self.render_to_response(context)

    def get_context_data(self):
        basket = BasketItem.objects.user_items_dict(self.request.user)

        def price_to_object(price):
            return price.stock_unit.stock, {
                'stock_unit': price.stock_unit,
                'price': price.price,
                'user_price': price.user_price(),
                'quantity': basket.get(price.stock_unit_id, BasketItem(quantity=0)).quantity,
                'quantity_reserved': price.stock_unit.quantity_reserved,
            }

        object_sort_key = lambda obj: obj['stock_unit'].product.part_number

        stocks = OrderedDict()
        replacement_stocks = OrderedDict()

        if self.part_number:
            clean_part_number = clear_part_number(self.part_number)

            price_type = get_user_price_type(self.request.user)

            prices = ProductStockUnitPrice.objects.filter(
                price_type=price_type,
                stock_unit__load_state__gte=0,
                stock_unit__product__part_number_search__startswith=clean_part_number
            ).distinct(
            )[:10].select_related()
            stocks = get_stocks(stock_items(prices, price_to_object), object_sort_key)

            replacement_prices = ProductStockUnitPrice.objects.filter(
                price_type=price_type,
                stock_unit__load_state__gte=0,
                stock_unit__product__replacements__part_number_search__startswith=clean_part_number
            ).exclude(
                stock_unit__product__part_number_search__startswith=clean_part_number
            ).distinct(
            )[:20].select_related()
            replacement_stocks = get_stocks(stock_items(replacement_prices, price_to_object), object_sort_key)

        context = {
            'stock_list': stocks,
            'replacement_list': replacement_stocks,
            'part_number': self.part_number,
        }

        return context


class AddBasketItem(LoginRequiredMixin, JSONResponseMixin, View):

    def post(self, request, *args, **kwargs):
        item_data = self._parse_request()
        self._add_basket_item(item_data)

        desc = catalogtags.basket_stats(Context({'request': self.request}))
        return self.render_to_response({'desc': desc})

    def _parse_request(self):
        stock_unit_id = int(self.request.POST['stock_unit_id'])
        customer = self.request.user
        try:
            quantity = parse_quantity(self.request.POST['quantity'])
        except (ValueError, InvalidOperation):
            quantity = 0
        is_replacement = self.request.POST.get('is_replacement', '').lower() == 'true'

        return {'customer': customer,
                'stock_unit_id': stock_unit_id,
                'quantity': quantity,
                'is_replacement': is_replacement}

    @staticmethod
    def _add_basket_item(item_data):
        try:
            BasketItem.objects.put(**item_data)
        except BasketItem.DoesNotExist:
            pass


class BasketSave(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        BasketItem.objects.update_basket(self.request.user, self._parse_post())

        if self.request.POST.has_key('order'):
            url = reverse('catalog:order')
        else:
            url = reverse('catalog:basket')

        return http.HttpResponseRedirect(url)

    def _parse_post(self):
        items = {}
        for key, value in self.request.POST.iteritems():
            if key.startswith('quantity') or key.startswith('selected') or key.startswith('deleted'):
                name, id = key.split('__', 1)
                id = int(id)
                item = items.get(id, {'quantity': 0, 'selected': False, 'deleted': False})
                item[name] = parse_quantity(value) if name=='quantity' else True
                items[id] = item
        return items


class BasketBase(object):

    stock_names = ['stock_list_available', 'stock_list_setapart', 'stock_list_disabled']

    def get_context_data(self, **kwargs):
        map = {
            'stock_unit_id': 'stock_unit_id',
            'stock_unit__stock': 'stock',
            'stock_unit__pending': 'pending',
            'stock_unit__quantity': 'stock_quantity',

            'stock_unit__product__id': 'product_id',
            'stock_unit__product__code': 'code',
            'stock_unit__product__part_number': 'part_number',
            'stock_unit__product__name': 'name',

            'stock_unit__basketitem__id': 'id',
            'stock_unit__basketitem__quantity': 'basket_quantity',
            'stock_unit__basketitem__selected': 'selected',
            'stock_unit__basketitem__is_replacement': 'is_replacement',

            'unit': 'unit',
            'multiplier': 'multiplier',
            'price': 'price',
        }

        self.basket_changed = False

        def item_to_object(item):
            stock = item['stock_unit__stock']
            obj = map_dict(map, item)
            obj['user_price'] = get_user_price(item['price'], item['price_type__currency_rate'])

            if obj['stock_quantity'] < obj['basket_quantity']:
                basket_item = BasketItem.objects.get(id=obj['id'])
                basket_item.quantity = obj['stock_quantity']
                basket_item.save()
                self.basket_changed = True

            obj['basket_quantity'] = min(obj['basket_quantity'], obj['stock_quantity'])
            obj['basket_cost'] = obj['user_price'] * obj['basket_quantity']
            return stock, obj

        object_sort_key=operator.itemgetter('part_number')

        prices, price_type = BasketItem.objects.prices(self.request.user)
        items = prices.values(*(map.keys() + ['price_type__currency_rate']))

        stocks = {name: [] for name in self.stock_names}

        for item in items:
            if stock_unit_can_be_ordered(item):
                if item['stock_unit__basketitem__selected'] and item['stock_unit__quantity'] > 0 and item['stock_unit__basketitem__quantity'] > 0:
                    stocks['stock_list_available'].append(item)
                else:
                    stocks['stock_list_setapart'].append(item)
            else:
                stocks['stock_list_disabled'].append(item)

        context = {key: get_stocks(stock_items(items, item_to_object), object_sort_key) for key, items in stocks.iteritems()}
        context['total_available_count'] = sum(item['basket_quantity'] for stock in context['stock_list_available'].itervalues() for item in stock['objects'])
        context['total_available_sum'] = sum(item['basket_cost'] for stock in context['stock_list_available'].itervalues() for item in stock['objects'])
        context['price_type'] = price_type

        context.update(kwargs)

        if self.basket_changed:
            messages.info(self.request, u"Количество товаров, доступных для заказа, уменьшилось. Возможно, кто-то только что зарезервировал товары.\n\nСостав корзины был изменён! Проверьте количество товаров ещё раз!")

        return context


class Basket(LoginRequiredMixin, BasketBase, NavigationTemplateView):
    template_name = 'catalog/basket.html'
    trail_parent = HomeNavigationView
    trail = StaticNode(u"Корзина", 'catalog:basket')


class UploadForm(LoginRequiredMixin, NavigationFormView):
    form_class = UploadFileForm
    template_name = 'catalog/upload_form.html'
    success_url = reverse_lazy('catalog:upload_basket')
    trail_parent = HomeNavigationView
    trail = StaticNode(u"Загрузка заказа", 'catalog:upload_basket')

    def form_valid(self, form):
        cleaned_data = form.cleaned_data['file']
        self.request.session['parsed_upload'] = cleaned_data
        return super(UploadForm, self).form_valid(form)


class UploadBasket(LoginRequiredMixin, NavigationTemplateView):
    template_name = 'catalog/upload_basket.html'
    trail_parent = HomeNavigationView
    trail = StaticNode(u"Обработка загрузки заказа", 'catalog:upload_basket')

    def get(self, request, *args, **kwargs):
        self.parsed_upload = self.request.session['parsed_upload']
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        map = {
            'stock_unit_id': 'stock_unit_id',
            'stock_unit__stock': 'stock',
            'stock_unit__pending': 'pending',
            'stock_unit__quantity': 'stock_quantity',
            'stock_unit__quantity_reserved': 'quantity_reserved',

            'stock_unit__product__id': 'product_id',
            'stock_unit__product__code': 'code',
            'stock_unit__product__part_number': 'part_number',
            'stock_unit__product__name': 'name',

            'unit': 'unit',
            'multiplier': 'multiplier',
            'price': 'price',
        }

        def item_to_object(item):
            stock = item['stock_unit__stock']
            obj = map_dict(map, item)
            obj['user_price'] = get_user_price(item['price'], item['price_type__currency_rate'])
            obj['quantity'] = 0

            return stock, obj

        object_sort_key = operator.itemgetter('sort_key')

        stock_order = lambda s: -1 if s == 1 else s # First goes main stock
        part_item_sort_key = lambda i: (stock_order(i[0]), i[1]['part_number'])

        price_type = get_user_price_type(self.request.user)

        items = []
        for part_number, quantity in self.parsed_upload:
            clean_part_number = clear_part_number(part_number)

            prices = ProductStockUnitPrice.objects.filter(price_type=price_type, stock_unit__product__part_number_search=clean_part_number, stock_unit__load_state__gte=0).select_related()
            part_items = stock_items(prices.values(*(map.keys() + ['price_type__currency_rate'])), item_to_object)
            part_items = sorted(part_items, key=part_item_sort_key)
            if len(part_items) > 0:
                part_item = part_items[0][1]
                part_item['quantity'] = min(part_item['stock_quantity'], quantity)
            for stock, part_item in part_items:
                part_item['sort_key'] = part_number
                part_item['is_replacement'] = False

            items += part_items

            replacement_prices = ProductStockUnitPrice.objects.filter(price_type=price_type, stock_unit__load_state__gte=0, stock_unit__product__replacements__part_number_search=clean_part_number).select_related()
            part_replacement_items = list(stock_items(replacement_prices.values(*(map.keys() + ['price_type__currency_rate'])), item_to_object))
            part_replacement_items = filter(lambda i: i[1]['stock_quantity'] > 0, part_replacement_items)
            for stock, part_item in part_replacement_items:
                part_item['sort_key'] = u'{}__{}'.format(part_number, part_item['part_number'])
                part_item['is_replacement'] = True

            items += part_replacement_items

        context = {
            'stock_list': get_stocks(items, object_sort_key),
        }

        return context


class UploadSave(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        for id, item in six.iteritems(self._parse_post()):
            BasketItem.objects.put(self.request.user, id, **item)

        self.request.session['parsed_upload'] = []

        return http.HttpResponseRedirect(reverse('catalog:basket'))

    def _parse_post(self):
        items = {}
        for key, value in six.iteritems(self.request.POST):
            if key.startswith('item'):
                name, id, replacement = key.split('__')
                items[int(id)] = {'quantity': parse_quantity(value), 'is_replacement': len(replacement) > 0}
        return items


class ValidationException(Exception):

    def __init__(self, msg=None):
        self.msg = msg
        super(ValidationException, self).__init__(msg)

    def __str__(self):
        return self.msg


class OrderMake(LoginRequiredMixin, BasketBase, NavigationCreateView):
    template_name = 'catalog/order.html'
    trail_parent = HomeNavigationView
    trail = StaticNode(u"Оформление заказа", 'catalog:order')
    form_class = OrderForm

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            try:
                self.validate()
            except ValidationException as e:
                if e.msg:
                    messages.info(request, e.msg)
                return self.form_invalid(form)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def validate(self):
        self.context = self.get_context_data()

        if self.basket_changed:
            raise ValidationException()

        total_quantity = 0
        with transaction.commit_on_success():
            for stock_id, stock in self.context['stock_list_available'].iteritems():
                for item in stock['objects']:
                    try:
                        stock_unit_reserve(item['stock_unit_id'], item['basket_quantity'])
                    except ReserveException:
                        raise ValidationException(u"Количество товаров в заказе превышает количество товаров на складе, пожалуйста, проверьте позиции заказа.")
                    total_quantity += item['basket_quantity']
            if total_quantity == 0:
                raise ValidationException(u"Количество товаров в заказе нулевое, пожалуйста, вернитесь в корзину и сформируйте непустой заказ.")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.customer = self.request.user
        self.object.status = 1
        self.object.currency = self.context['price_type'].currency
        self.object.currency_rate =  self.context['price_type'].currency_rate
        self.object.sum = self.context['total_available_sum']
        self.object.save()

        for stock_id, stock in self.context['stock_list_available'].iteritems():
            for item in stock['objects']:
                order_item = OrderItem(order=self.object)
                order_item.code = item['code']
                order_item.part_number = item['part_number']
                order_item.name = item['name']
                order_item.stock = stock_id
                order_item.pending = item['pending']
                order_item.price = item['price']
                order_item.user_price = item['user_price']
                order_item.quantity = item['basket_quantity']
                order_item.sum = item['basket_cost']
                order_item.unit = item['unit']
                order_item.multiplier = item['multiplier']
                order_item.is_replacement = item['is_replacement']
                order_item.save()

                BasketItem.objects.filter(id=item['id']).delete()

        try:
            send_order_to_customer(self.object)
        except SMTPException:
            messages.info(self.request, u"К сожалению, мы не смогли выслать подтверждение на ваш e-mail, но вы можете посмотреть статус Вашего заказа на странице заказов.")

        send_order_to_admin(self.object)

        return super(OrderMake, self).form_valid(form)


class OrderDetail(LoginRequiredMixin, BasketBase, NavigationDetailView):
    model = Order
    template_name = 'catalog/order_detail.html'

    def get(self, request, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.customer:
            raise Http404
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):

        def item_to_object(item):
            stock = item.stock
            return stock, item

        def object_sort_key(item):
            return item.part_number

        items = OrderItem.objects.filter(order=self.object).select_related()
        context = {'stock_list': get_stocks(stock_items(items, item_to_object), object_sort_key)}
        context['total_count'] = sum(item.quantity for stock in context['stock_list'].itervalues() for item in stock['objects'])
        context['total_sum'] = sum(item.sum for stock in context['stock_list'].itervalues() for item in stock['objects'])
        context.update(kwargs)
        return context


class OrderDetailExcel(OrderDetail):

    def render_to_response(self, context, **response_kwargs):
        import StringIO
        output = StringIO.StringIO()
        workbook = xlwt.Workbook(encoding='utf-8')

        file_name = 'order_{}'.format(self.kwargs['pk'])
        sheet = workbook.add_sheet(file_name)

        font = xlwt.Font()
        font.name = 'Arial'
        font.bold = True

        style = XFStyle()
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        style.alignment = alignment
        style.font = font # Apply the Font to the Style
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green,
        # 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow ,
        # almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
        pattern.pattern_fore_colour = 22
        style.pattern = pattern

        style_1=XFStyle()
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        style_1.alignment = alignment
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        borders = xlwt.Borders() # Create Borders
        borders.left = xlwt.Borders.DASHED # May be: NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR,
        # MEDIUM_DASHED, THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED,
        # SLANTED_MEDIUM_DASH_DOTTED, or 0x00 through 0x0D.
        borders.right = xlwt.Borders.DASHED
        borders.top = xlwt.Borders.DASHED
        borders.bottom = xlwt.Borders.DASHED
        borders.left_colour = 0x40
        borders.right_colour = 0x40
        borders.top_colour = 0x40
        borders.bottom_colour = 0x40
        style_1.borders = borders
        style_1.font = font

        style_2=XFStyle()
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_RIGHT
        style_2.alignment = alignment

        style_3=XFStyle()
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_RIGHT
        style_3.alignment = alignment
        style_3.font = font
        pattern.pattern_fore_colour = 22
        style_3.pattern = pattern

        style_4=XFStyle()
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        style_4.alignment = alignment

        sheet.col(0).width = 4333 # 3333 = 1" (one inch).
        sheet.col(1).width = 11333
        sheet.col(2).width = 3333
        sheet.col(3).width = 3333
        sheet.col(5).width = 4333
        sheet.col(6).width = 3133

        sheet.write(2, 0, u'Код по каталогу', style_1)
        sheet.write(2, 1, u'Название', style_1)
        sheet.write(2, 2, u'Цена, USD', style_1)
        sheet.write(2, 3, u'Цена, UAH', style_1)
        sheet.write(2, 4, u'Кол-во', style_1)
        sheet.write(2, 5, u'Сумма, UAH', style_1)
        sheet.write(2, 6, u'Наличие', style_1)

        row = 3
        sheet.write_merge(0, 1, 0, 6, '{}'.format(context['object']), style_1)
        for stock in context['stock_list'].itervalues():
            sheet.write_merge(row, row, 0, 6, stock['name'], style)
            row += 1
            for object in stock['objects']:
                sheet.write(row, 0, object.part_number, style_4)
                sheet.write(row, 1, object.name)
                sheet.write(row, 2, object.price, style_2)
                sheet.write(row, 3, object.user_price, style_2)
                sheet.write(row, 4, object.quantity, style_2)
                sheet.write(row, 5, object.sum.normalize(), style_2)
                if object.pending:
                    sheet.write(row, 6, object.pending.strftime("%Y-%m-%d"), style_4)
                else:
                    sheet.write(row, 6, '+', style_4)
                row += 1
        sheet.write_merge(row, row, 0, 3, u'Всего', style)
        sheet.write(row, 4, int(context['total_count']), style_3)
        sheet.write(row, 5, Decimal(context['total_sum']).normalize(), style_3)
        sheet.write(row, 6, u'', style_3)

        workbook.save(output)
        mimetype = 'application/vnd.ms-excel'
        response = HttpResponse(output.getvalue(),mimetype)
        response['Content-Disposition'] = 'attachment;filename="{}.xls"'.format(file_name)
        return response


class OrderList(LoginRequiredMixin, NavigationListView):
    model = Order
    trail_parent = HomeNavigationView
    trail = StaticNode(u"История заказов", 'catalog:order_list')
    template_name = 'catalog/order_list.html'

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)


class Exchange(View):

    def dispatch(self, request, *args, **kwargs):

        def query():
            return ComplexExporter().build()

        def success():
            return ExporterSuccess().build()

        modes = {
            'query': query,
            'success': success,
        }

        mode = request.GET['mode']

        result = run_exchange(request, modes.get(mode))
        response = HttpResponse()
        response['charset'] = 'windows-1251'
        response.write(result.encode('cp1251', errors='ignore'))
        return response
