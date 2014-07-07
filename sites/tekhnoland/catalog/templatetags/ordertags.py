# coding=utf-8
from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag(takes_context=True)
def order_headrow(context):
    return render_to_string('catalog/order_headrow.html', context_instance=context)

@register.simple_tag(takes_context=True)
def order_textrow(context, cls, text):
    context['text'] = text
    context['class'] = cls
    return render_to_string('catalog/order_textrow.html', context_instance=context)

@register.simple_tag(takes_context=True)
def order_datarow(context, object):
    context['object'] = object
    return render_to_string('catalog/order_datarow.html', context_instance=context)

@register.simple_tag(takes_context=True)
def orderitem_datarow(context, object):
    context['object'] = object
    return render_to_string('catalog/orderitem_datarow.html', context_instance=context)
