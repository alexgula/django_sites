# coding=utf-8
from django import template
from django.contrib.sites.models import get_current_site

from .. import liqpay


register = template.Library()


@register.inclusion_tag('shop/liqpay_form.html')
def liqpay_form(request, order):
    site = get_current_site(request)
    data = liqpay.get_payment_data(site, order)
    return {'data': data, 'lang': 'ru'}
