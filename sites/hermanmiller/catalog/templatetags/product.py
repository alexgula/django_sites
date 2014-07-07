# coding=utf-8
from django import template
from mediatools.templatetags import extract_context
from ..models import Product

register = template.Library()


@register.inclusion_tag('catalog/product_special.html', takes_context=True)
@extract_context('settings')
def products_special(context, count):
    return {'objects': Product.objects.special()[:count]}


@register.inclusion_tag('catalog/product_blocks.html', takes_context=True)
@extract_context('settings')
def products(context, obj):
    return {'objects': obj}
