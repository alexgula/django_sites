# coding=utf-8
import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language

from feincms.models import create_base_model
from mptt.models import MPTTModel
from sorl.thumbnail import ImageField
from localeurl.templatetags.localeurl_tags import rmlocale

from picassoft.utils.views import permalink
from ..managedimage.models import upload_path
from ..search.util import TranslatedUnicode

REGION_TYPES = [
    ('town', _("Town")),
    ('district', _("District")),
]

TRACK_PLACE_SITESEEING = 1
TRACK_PLACE_CATERING = 2

TRACK_PLACE_TYPES = [
    (TRACK_PLACE_SITESEEING, _("Siteseeing")),
    (TRACK_PLACE_CATERING, _("Catering")),
]

class Region(create_base_model()):
    type = models.CharField(_("Type"), max_length=10, choices=REGION_TYPES)
    name = models.CharField(_("Name"), max_length=150)
    slug = models.SlugField(_("Slug"))
    icon = ImageField(_("Icon"), max_length=250, upload_to=upload_path('{class_path}/icon/{slug}'), blank=True)
    desc = models.TextField(_("Description"), blank=True)
    map_id = models.PositiveIntegerField(_("Map ID"), blank=True, null=True)
    map_color = models.CharField(_("Map Color"), max_length=12, blank=True)

    class Meta:
        ordering = ['name']
        unique_together = ['type', 'slug']

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return 'region_detail', None, dict(type_slug=self.type, slug=self.slug)


class PlaceType(MPTTModel):
    name = models.CharField(_("Name"), max_length=150)
    slug = models.SlugField(_("Slug"))
    parent = models.ForeignKey('self', verbose_name=_("Parent"), null=True, blank=True, related_name='children')
    active = models.BooleanField(_("Active"), default=True)
    code = models.PositiveIntegerField(_("Integration code"), blank=True, null=True)
    icon = ImageField(_("Icon"), max_length=250, upload_to=upload_path('{class_path}/icon/{slug}'), blank=True)
    show_extra = models.BooleanField(_("Show extra contacts"), default=False, help_text=_("Show extra information like phones etc."))

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return 'place_list', None, dict(type_slug=self.slug)


class Place(MPTTModel):
    type = models.ForeignKey(PlaceType, verbose_name=_("Type"))
    name = models.CharField(_("Name"), max_length=150, db_index=True)
    slug = models.SlugField(_("Slug"))
    address = models.TextField(_("Address"), blank=True)
    phone = models.CharField(_("Phone"), max_length=250, blank=True)
    timetable = models.CharField(_("Timetable"), max_length=250, blank=True)
    url = models.URLField(_("URL"), blank=True)
    exposition = models.TextField(_("Exposition"), blank=True)
    transport = models.TextField(_("Transport"), blank=True)
    desc = models.TextField(_("Description"), blank=True)
    image = ImageField(_("Image"), max_length=250, upload_to=upload_path('{class_path}/image/{slug}'), blank=True)
    parent = models.ForeignKey('self', verbose_name=_("Parent"), null=True, blank=True, related_name='children')
    active = models.BooleanField(_("Active"), default=True)
    interop_code = models.CharField(_("Integration code"), max_length=20, blank=True, null=True)
    lon = models.FloatField(_("Longitude"), blank=True, null=True)
    lat = models.FloatField(_("Latitude"), blank=True, null=True)
    audio_index = models.CharField(_("Audio Guide"), max_length=20, blank=True, help_text=_("Audio guide file."))

    class Meta:
        ordering = ['name']
        unique_together = [['type', 'slug'], ]

    def __unicode__(self):
        parts = [self.name]
        if self.address:
            parts.append(self.address)
        return u", ".join(parts)

    def save(self, *args, **kwargs):
        if len(self.url) > 0 and not (self.url.startswith(u"http") or self.url.startswith(u"https")):
            self.url = u"http://" + self.url
        super(Place, self).save(*args, **kwargs)

    @permalink
    def get_absolute_url(self):
        return 'place_detail', None, dict(type_slug=self.type.slug, slug=self.slug)

    def image_path(self):
        """Build image path parameters for ImageField file name resolver."""
        id = unicode(uuid.uuid4())
        params = {
            'path': id[:2],
            'uuid': id,
        }
        return params

    def get_nonlocal_url(self):
        return rmlocale(self.get_absolute_url())

    def get_name_translations(self):
        result = TranslatedUnicode()
        result.add_field_translations(self, 'name')
        return result

    def get_type_translations(self):
        result = TranslatedUnicode()
        result.add_field_translations(self.type, 'name')
        return result

    def get_desc_translations(self):
        result = TranslatedUnicode()
        result.add_field_translations(self, 'desc')
        return result

    def get_text_translations(self):
        result = self.get_desc_translations()
        result.add(self.get_type_translations())
        result.add_field_translations(self, 'name')
        result.add_field_translations(self, 'address')
        result.add_field_translations(self, 'phone')
        result.add_field_translations(self, 'exposition')
        result.add_text(self.slug)
        return result

    def audio_url(self):
        return u'audioguide/{}/{}.mp3'.format(get_language(), self.audio_index)


class Track(models.Model):
    name = models.CharField(_("Name"), max_length=150, db_index=True)
    slug = models.SlugField(_("Slug"))
    track = models.CharField(_("Track"), max_length=1000)
    duration = models.PositiveIntegerField(_("Duration"), blank=True, null=True)
    length = models.PositiveIntegerField(_("Length"), blank=True, null=True)
    places = models.ManyToManyField(Place, through='TrackPlaces', verbose_name=_("Places"), blank=True)
    image_desc = models.ImageField(_("Description image"), max_length=250, upload_to=upload_path('{class_path}/image_desc/{path}/{uuid}', params_extend='image_path'), blank=True)
    image_track = models.ImageField(_("Track image"), max_length=250, upload_to=upload_path('{class_path}/image_track/{path}/{uuid}', params_extend='image_path'), blank=True)
    video = models.FileField(_("Video"), upload_to=upload_path('{class_path}/video/{path}/{uuid}', params_extend='image_path'), blank=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return 'track_detail', None, dict(slug=self.slug)

    def image_path(self):
        """Build image path parameters for ImageField file name resolver."""
        id = unicode(uuid.uuid4())
        params = {
            'path': id[:2],
            'uuid': id,
        }
        return params

    def get_places(self, **kwargs):
        return Place.objects.filter(trackplaces__track=self, **kwargs).order_by('trackplaces__order')

    def get_siteseeing(self):
        return self.get_places(trackplaces__type=TRACK_PLACE_SITESEEING)

    def get_catering(self):
        return self.get_places(trackplaces__type=TRACK_PLACE_CATERING)


class TrackPlaces(models.Model):
    track = models.ForeignKey(Track, verbose_name=_("Track"))
    place = models.ForeignKey(Place, verbose_name=_("Place"))
    order = models.IntegerField(_("Order"))
    type = models.IntegerField(_("Type"), default=1, choices=TRACK_PLACE_TYPES)

    class Meta:
        ordering = ['order']
