# coding=utf-8
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.conf import settings
from picassoft.utils.mail import send_html_mail
from .models import OrderItem, get_stocks, stock_items

def send_order_to_customer(order):
    current_site = Site.objects.get(id=settings.SITE_ID)

    subject = u"Tekhnoland: заказ {}".format(order)
    from_email = settings.ORDER_SENDER

    def item_to_object(item):
        stock = item.stock
        return stock, item

    def object_sort_key(item):
        return item.part_number

    items = OrderItem.objects.filter(order=order).select_related()

    context = {'object': order, 'stock_list': get_stocks(stock_items(items, item_to_object), object_sort_key), 'site': current_site}
    context['total_count'] = sum(item.quantity for stock in context['stock_list'].itervalues() for item in stock['objects'])
    context['total_sum'] = sum(item.sum for stock in context['stock_list'].itervalues() for item in stock['objects'])

    message = render_to_string('catalog/order_email.html', context)
    recipient_list = [order.customer.email]

    return send_html_mail(subject, message, from_email, recipient_list)

def send_order_to_admin(order):
    current_site = Site.objects.get(id=settings.SITE_ID)

    subject = u"Новый заказ на сайте Tekhnoland"
    from_email = settings.ORDER_SENDER

    def item_to_object(item):
        stock = item.stock
        return stock, item

    def object_sort_key(item):
        return item.part_number

    items = OrderItem.objects.filter(order=order).select_related()

    context = {'object': order, 'stock_list': get_stocks(stock_items(items, item_to_object), object_sort_key), 'site': current_site}
    context['total_count'] = sum(item.quantity for stock in context['stock_list'].itervalues() for item in stock['objects'])
    context['total_sum'] = sum(item.sum for stock in context['stock_list'].itervalues() for item in stock['objects'])

    message = render_to_string('catalog/order_notification_email.html', context)
    recipient_list = settings.ORDER_RECIPIENTS

    return send_html_mail(subject, message, from_email, recipient_list)
