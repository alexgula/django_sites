# coding=utf-8
from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag(takes_context=True)
def basket_headrow(context):
    return render_to_string('catalog/basket_headrow.html', context_instance=context)

@register.simple_tag(takes_context=True)
def basket_textrow(context, cls, text):
    context['text'] = text
    context['class'] = cls
    return render_to_string('catalog/basket_textrow.html', context_instance=context)

@register.simple_tag(takes_context=True)
def basket_datarow(context, object):
    context['object'] = object
    return render_to_string('catalog/basket_datarow.html', context_instance=context)
