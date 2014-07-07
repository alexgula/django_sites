# coding=utf-8
from django.core.exceptions import ObjectDoesNotExist
from django import template
from ..models import Currency
from modeltranslation.utils import get_language

register = template.Library()


@register.inclusion_tag('currency_rates.html')
def currency_rates():
    current_lang = get_language()
    currencies = Currency.objects.all()
    currencies_other = []
    currency_current = None
    for currency in currencies:
        if currency.lang == current_lang:
            currency_current = currency
        else:
            currencies_other.append(currency)
    if currency_current is None:
        currency_current = currencies_other.pop(0)
    return dict(current=currency_current, currencies=currencies_other)
