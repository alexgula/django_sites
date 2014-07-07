# coding=utf-8
from django import template
from ..util import TranslatedUnicode

register = template.Library()

@register.filter
def translate(text, lang_code=None):
    tstr = TranslatedUnicode(text)
    return tstr.translate(lang_code)
