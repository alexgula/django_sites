# coding=utf-8
from django.core.exceptions import ValidationError
from picassoft.utils.templatetags.markup import restructuredtext


def validate_rst(text):
    try:
        restructuredtext(text)
    except Exception as e:
        raise ValidationError(u"Restructured text error!\n{}".format(e))
