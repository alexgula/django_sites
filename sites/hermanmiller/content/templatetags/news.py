# coding=utf-8
from django import template
from ..models import News

register = template.Library()

@register.inclusion_tag('content/news_latest.html')
def news_latest(count):
    return {'news_list': News.objects.order_by('-created_on')[:count]}
