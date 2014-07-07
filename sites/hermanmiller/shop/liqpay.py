# coding=utf-8
import base64
import hashlib
from django.core.urlresolvers import reverse
from constance import config
from .models import Order


def get_payment_data(site, order):
    data = {
        'amount': u"1",#u"{:.2f}".format(order.sum_uah).replace(',', '.'),
        'currency': 'UAH',
        'public_key': config.LIQPAY_PUBLIC_KEY,
        'order_id': u"{}".format(order.id),
        'type': 'buy',
        'description': u"{}".format(order),
        'result_url': "http://{}{}".format(site.domain, order.get_absolute_url()),
        'server_url': "http://{}{}".format(site.domain, reverse('shop_order_liqpay_confirm', kwargs={'pk': order.pk})),
    }
    data['signature'] = _get_payment_signature(data)
    return data


def verify_signature(data):
    return _get_verification_signature(data) == data['signature']


def _get_verification_data(order_id):
    order = Order.objects.get(pk=order_id)
    data = {
        'amount': u"{}".format(order.sum_uah),
        'currency': 'UAH',
        'public_key': config.LIQPAY_PUBLIC_KEY,
        'order_id': u"{}".format(order.pk),
        'type': 'buy',
        'description': u"{}".format(order),
        'status': 'success',
        'transaction_id': u"{}".format(order.pk),
        'sender_phone': '099'}
    data['signature'] = _get_verification_signature(data)
    return data


def _get_payment_signature(data):
    data_string = "".join([
        config.LIQPAY_PRIVATE_KEY,
        data['amount'],
        data['currency'],
        data['public_key'],
        data['order_id'],
        data['type'],
        data['description'],
        data['result_url'],
        data['server_url']])
    return _encode(data_string)


def _get_verification_signature(data):
    data_string = u"".join([
        config.LIQPAY_PRIVATE_KEY,
        data['amount'],
        data['currency'],
        data['public_key'],
        data['order_id'],
        data['type'],
        data['description'],
        data['status'],
        data['transaction_id'],
        data['sender_phone']])
    return _encode(data_string)


def _encode(data_string):
    return base64.b64encode(hashlib.sha1(data_string).digest())
