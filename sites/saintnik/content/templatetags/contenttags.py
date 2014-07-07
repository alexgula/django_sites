# coding=utf-8
from django import template
from ..models import News

register = template.Library()


@register.inclusion_tag('content/news_block_list.html')
def latest_news(count):
    news_list = News.objects.filter(active=True)[:count]
    return dict(news_list=news_list)
