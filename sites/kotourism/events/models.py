# coding=utf-8
import datetime
import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy

from feincms.models import create_base_model
from sorl.thumbnail import ImageField
from localeurl.templatetags.localeurl_tags import rmlocale

from picassoft.utils.views import permalink
from ..managedimage.models import upload_path
from ..places.models import Place
from ..search.util import TranslatedUnicode


# Using context to avoid news pluralization error in search
EVENT_TYPES_SOURCE = [
    ('announce', "Announce"),
    ('event', "Event"),
    ('news', "News"),
]

EVENT_TYPES = [(code, pgettext_lazy('singular', name)) for code, name in EVENT_TYPES_SOURCE]

# Noop just to generate translations
pgettext_lazy('singular', "Announce")
pgettext_lazy('singular', "Event")
pgettext_lazy('singular', "News")
pgettext_lazy('plural', "Announce")
pgettext_lazy('plural', "Event")
pgettext_lazy('plural', "News")


class EventManager(models.Manager):

    def active(self):
        return self.get_query_set().filter(active=True)


class Event(create_base_model()):
    type = models.CharField(_("Type"), choices=EVENT_TYPES, max_length=10, db_index=True)
    name = models.CharField(_("Name"), max_length=250)
    slug = models.SlugField(_("Slug"))
    active = models.BooleanField(_("Active"), default=True)
    date_active_from = models.DateField(_("Date Active From"), blank=True, null=True)
    date_from = models.DateField(_("Date From"))
    date_to = models.DateField(_("Date To"), blank=True, null=True)
    icon = ImageField(_("Icon"), max_length=250, upload_to=upload_path('{class_path}/image/{path}/{uuid}', params_extend='image_path'), blank=True)
    desc = models.TextField(_("Description"), blank=True)
    place = models.CharField(_("Place"), max_length=250, blank=True)
    place_link = models.ForeignKey(Place, verbose_name=_("Place Link"), blank=True, null=True)
    organizer = models.CharField(_("Organizer"), max_length=250, blank=True)
    post_date = models.DateTimeField(_("Post Date"), auto_now_add=True, db_index=True)

    objects = EventManager()

    class Meta():
        verbose_name = _("event")
        verbose_name_plural = _("events")
        ordering = ['-post_date']
        unique_together = ('type', 'date_from', 'slug', )

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.date_from:
            self.date_from = datetime.date.today()
        if not self.date_to:
            self.date_to = self.date_from

        super(Event, self).save(*args, **kwargs)

    @permalink
    def get_absolute_url(self):
        year, month, day = self.slug_date()
        return 'event_detail', None, dict(type_slug=self.type, year=year, month=month, day=day, slug=self.slug, )

    def get_nonlocal_url(self):
        return rmlocale(self.get_absolute_url())

    def slug_date(self):
        slug_date = self.date_from
        year = u'{:#04}'.format(slug_date.year)
        month = u'{:#02}'.format(slug_date.month)
        day = u'{:#02}'.format(slug_date.day)
        return year, month, day

    def image_path(self):
        """Build image path parameters for ImageField file name resolver."""
        id = unicode(uuid.uuid4())
        params = {
            'path': id[:2],
            'uuid': id,
        }
        return params

    def get_name_translations(self):
        result = TranslatedUnicode()
        result.add_field_translations(self, 'name')
        return result

    def get_type_translations(self):
        result = TranslatedUnicode()
        result.add_text_translations(dict(EVENT_TYPES_SOURCE)[self.type], 'singular')
        return result

    def get_desc_translations(self):
        result = TranslatedUnicode()
        result.add_field_translations(self, 'desc')
        result.add_content_translations(self)
        return result

    def get_text_translations(self):
        result = self.get_desc_translations()
        result.add(self.get_type_translations())
        result.add_field_translations(self, 'name')
        result.add_text(self.slug)
        return result
