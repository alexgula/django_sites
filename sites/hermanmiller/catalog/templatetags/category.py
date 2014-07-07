# coding=utf-8
from django import template
from ..models import Category

register = template.Library()


@register.inclusion_tag('catalog/category_menu.html')
def category_menu():
    categories = Category.objects.root_nodes()
    return dict(category_menu=categories)
