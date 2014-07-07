# coding=utf-8
from decimal import Decimal
import re

WHITESPACES = re.compile(u'\s', flags=re.UNICODE)


def parse_quantity(quantity_string):
    return int(parse_decimal(quantity_string))


def parse_decimal(decimal_string):
    return Decimal(re.sub(WHITESPACES, '', decimal_string or '0').replace(',', '.'))
