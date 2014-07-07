# coding=utf-8
from django import template

register = template.Library()

@register.inclusion_tag('meteoprog.html')
def meteoprog(lang, country, city, color, txtcolor, bgcolor):
    return dict(lang=lang, country=country, city=city, color=color, txtcolor=txtcolor, bgcolor=bgcolor, )
