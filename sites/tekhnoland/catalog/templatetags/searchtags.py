# coding=utf-8
from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag(takes_context=True)
def search_headrow(context):
    return render_to_string('catalog/search_headrow.html', context_instance=context)

@register.simple_tag(takes_context=True)
def search_textrow(context, cls, text):
    context['text'] = text
    context['class'] = cls
    return render_to_string('catalog/search_textrow.html', context_instance=context)

@register.simple_tag(takes_context=True)
def search_datarow(context, object, cls=u''):
    context['object'] = object
    context['class'] = cls
    return render_to_string('catalog/search_datarow.html', context_instance=context)
