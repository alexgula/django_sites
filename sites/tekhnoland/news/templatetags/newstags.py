# coding=utf-8
from datetime import datetime

from django import template
from django.conf import settings
from django.db.models.query_utils import Q

from ..models import News

register = template.Library()


@register.inclusion_tag('news/news_short_list.html')
def latest_news(count):
    events = News.objects.filter(active=True)[:count]
    return dict(events=events)
