# coding=utf-8
from django import template
from ..models import Category

register = template.Library()


@register.inclusion_tag('catalog/top_categories.html')
def top_categories(count):
    categories = Category.objects.filter(active=True,show_on_main=True)[:count]
    return dict(top_categories=categories)