# coding=utf-8
from django import template
from django.template.loader import render_to_string
from ..models import BasketItem

register = template.Library()

@register.simple_tag(takes_context=True)
def basket_stats(context):
    user = context['request'].user
    context['basket_items'] = BasketItem.objects.filter(customer=user)
    item_sum, item_count = BasketItem.objects.stats(user)
    context['basket_sum'] = item_sum
    context['basket_count'] = item_count
    return render_to_string('catalog/basket_stats_block.html', context_instance=context)
