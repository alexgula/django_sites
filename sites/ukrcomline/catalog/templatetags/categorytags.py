# coding=utf-8
from django import template
from django.conf import settings
from picassoft.utils.itertools import tabulate
from ..models import Category

register = template.Library()

@register.inclusion_tag('catalog/category_menu.html')
def category_menu():
    column_count = settings.CATEGORY_MENU_COLUMN_COUNT
    category_tree = Category.objects.tree()
    return dict(category_menu=tabulate(category_tree, column_count))


@register.inclusion_tag('catalog/category_breadcrumbs.html')
def category_breadcrumbs(category):
    category_tree = Category.objects.tree()
    ancestors = category.get_ancestors()

    category_ancestors = []
    current_branch = category_tree
    for ancestor in ancestors:
        current = next((item for item in current_branch if item.key == ancestor.id))
        category_ancestors.append(current)
        current_branch = current.children

    return dict(category_ancestors=category_ancestors)


@register.inclusion_tag('catalog/category_breadcrumbs_recur.html')
def category_breadcrumbs_recur(item, level):
    return dict(parent_item=item, category_tree=item.children, level=level)
