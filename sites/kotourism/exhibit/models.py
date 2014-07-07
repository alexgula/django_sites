# coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField
from picassoft.files.storage import OverwritingStorage
from picassoft.utils.views import permalink

storage = OverwritingStorage()


class OrderedManager(models.Manager):

    def get_query_set(self):
        return super(OrderedManager, self).get_query_set().order_by('order')


class Exhibit(models.Model):
    name = models.CharField(_("Name"), max_length=250)
    slug = models.SlugField(_("Slug"))
    desc = models.TextField(_("Description"))
    active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Exhibition")
        verbose_name_plural = _("Exhibitions")

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return 'exhibit_detail', None, dict(slug=self.slug)


class ExhibitSection(models.Model):
    exhibit = models.ForeignKey(Exhibit, verbose_name=_("Exhibition"))
    order = models.IntegerField(_("Order"), default=0)
    name = models.CharField(_("Name"), max_length=250)
    desc = models.TextField(_("Description"))
    image = ImageField(_("Image"), upload_to='exhibit/section_image', storage=storage, blank=True, null=True)
    file = models.FileField(_("File"), upload_to='exhibit/section_file', storage=storage, blank=True, null=True)

    objects = OrderedManager()


class ExhibitMap(models.Model):
    exhibit = models.ForeignKey(Exhibit, verbose_name=_("Exhibition"))
    order = models.IntegerField(_("Order"), default=0)
    name = models.CharField(_("Name"), max_length=250)
    desc = models.TextField(_("Description"))
    lon = models.FloatField(_("Longitude"))
    lat = models.FloatField(_("Latitude"))

    objects = OrderedManager()


class ExhibitPartner(models.Model):
    exhibit = models.ForeignKey(Exhibit, verbose_name=_("Exhibition"))
    order = models.IntegerField(_("Order"), default=0)
    name = models.CharField(_("Name"), max_length=250)
    image = ImageField(_("Image"), upload_to='exhibit/partner', storage=storage)
    link = models.CharField(_("URL"), max_length=250)

    objects = OrderedManager()
