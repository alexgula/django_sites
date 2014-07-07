# coding=utf-8
from datetime import datetime

from django import template
from django.conf import settings
from django.db.models.query_utils import Q

from ..models import Event

register = template.Library()

@register.inclusion_tag('announce_list.html')
def announce():
    announces = Event.objects.filter(
        Q(type='announce'),
        Q(active=True),
        Q(date_active_from__lte=datetime.now()) | Q(date_from__lte=datetime.now()),
        Q(date_to__gt=datetime.now())
    )
    return dict(announces=announces)


@register.inclusion_tag('event_block_list.html')
def latest_news(count):
    events = Event.objects.filter(type='news', active=True).order_by('-post_date')[:count]
    return dict(events=events, THUMBNAIL_SETTINGS=settings.THUMBNAIL_SETTINGS)
