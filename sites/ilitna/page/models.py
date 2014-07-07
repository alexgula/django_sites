# coding=utf-8
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from feincms.models import create_base_model


class Page(create_base_model(MPTTModel)):
    """Information page."""
    slug = models.SlugField(_("Slug"), unique=True)
    title = models.CharField(_("Title"), max_length=250)
    parent = TreeForeignKey('self', verbose_name=_("Parent"), null=True, blank=True, related_name='children')

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return 'page:page', None, {'slug': self.slug}
