# coding=utf-8
import json
from django import template
from ..model_choices import PAYMENT_TYPE_CHOICES
from .. import session


register = template.Library()


@register.simple_tag
def cart_data(request):
    return json.dumps(session.cart.get_data(request))


@register.simple_tag
def cart_choices():
    return json.dumps({
        'payment_types': [{'id': item[0], 'name': item[1]} for item in PAYMENT_TYPE_CHOICES]
    })


@register.simple_tag
def is_authenticated(request):
    return 'true' if session.auth.is_authenticated(request) else 'false'


@register.simple_tag
def customer_name(request):
    customer = session.auth.get_data(request)
    return customer.name if customer is not None else u""
