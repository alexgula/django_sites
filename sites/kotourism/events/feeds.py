# coding=utf-8
from datetime import timedelta
from collections import namedtuple
from django.utils.timezone import now
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext, pgettext, get_language
from picassoft.utils.templatetags.markup import restructuredtext

from .models import Event, EVENT_TYPES_SOURCE

EVENT_TYPES = dict(EVENT_TYPES_SOURCE)

EventType = namedtuple('EventType', ['code', 'desc'])

class EventFeed(Feed):
    feed_type = Atom1Feed
    description = _("Updates on changes and additions to ko-tourism.gov.ua.")
    subtitle = description

    def get_object(self, request, type_slug):
        return EventType(type_slug, pgettext('plural', EVENT_TYPES[type_slug]))

    def title(self, obj):
        return ugettext("Latest tourists {} of Kyiv oblast.").format(obj.desc.lower())

    def link(self, obj):
        from django.core import urlresolvers
        return urlresolvers.reverse('typed_event_list', kwargs=dict(type_slug=obj.code))

    def items(self, obj):
        return Event.objects.active().filter(type=obj.code, post_date__gte=now()-timedelta(weeks=13)).order_by('-post_date')

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return restructuredtext(item.desc)

    def item_pubdate(self, item):
        return item.post_date
