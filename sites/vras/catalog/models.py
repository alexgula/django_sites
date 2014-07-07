# coding=utf-8
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    title = models.CharField(_("Title"), max_length=250)
    logo = models.ImageField(_("Logo"), max_length=250, upload_to='images', blank=True)
    desc = models.TextField(_("Description"), blank=True)
    slug = models.SlugField(_("Slug"), blank=True)
    active = models.BooleanField(_("Active"), default=True)
    parent = TreeForeignKey('self', verbose_name=_("Parent"), null=True, blank=True, related_name='children')

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return 'category_detail', None, dict(slug=self.slug)

    @property
    def first_image(self):
        try:
            return self.images.all()[0]
        except IndexError:
            return None


class CategoryImage(models.Model):
    category = TreeForeignKey(Category, verbose_name=_("Category"), related_name="images")
    image = models.ImageField(_("Image"), max_length=250, upload_to='images')
