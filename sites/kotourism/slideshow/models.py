# coding=utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..managedimage.models import upload_path
from picassoft.utils.models import ActiveManager


class Slide(models.Model):
    name = models.CharField(_("Name"), max_length=250)
    slug = models.SlugField(_("Slug"))
    active = models.BooleanField(_("Active"), default=True)
    desc = models.TextField(_("Description"), blank=True)
    slide = models.ImageField(_("Slide"), upload_to=upload_path('{class_path}/slide/{slug}'))
    icon = models.ImageField(_("Icon"), upload_to=upload_path('{class_path}/icon/{slug}'))
    map_lon = models.FloatField(_("Longitude"))
    map_lat = models.FloatField(_("Latitude"))

    objects = ActiveManager()

    def __unicode__(self):
        return self.name

    map_top = 51.515559
    map_right = 32.164757
    map_left = 29.451134
    map_bottom = 49.180056

    def map_x(self):
        """Get x on map from range [0; 1] from left to right."""
        left = self.map_lon - self.map_left
        width = self.map_right - self.map_left
        return left / width

    def map_y(self):
        """Get x on map from range [0; 1] from bottom to top."""
        bottom = self.map_lat - self.map_bottom
        height = self.map_top - self.map_bottom
        return bottom / height
