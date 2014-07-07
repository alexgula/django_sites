# coding=utf-8
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _


class ActiveObjectsManager(models.Manager):
    def active(self):
        return self.get_query_set().filter(active=True)


class CreatedObjectsManager(ActiveObjectsManager):
    def get_query_set(self):
        return super(CreatedObjectsManager, self).get_query_set().order_by('-created_on')


class BasicContent(models.Model):
    title = models.CharField(_("Title"), max_length=250)
    logo = models.ImageField(_("Logo"), max_length=250, upload_to='images', blank=True)
    desc = models.TextField(_("Description"), blank=True)
    active = models.BooleanField(_("Active"), default=True)

    def __unicode__(self):
        return self.title

    class Meta(object):
        abstract = True


class News(BasicContent):
    created_on = models.DateTimeField(_("Created On"))

    objects = CreatedObjectsManager()

    home_slug = 'news'

    @permalink
    def get_absolute_url(self):
        return 'news_detail', None, dict(pk=self.pk)

    class Meta(object):
        verbose_name_plural = _("News list")


class NewsImage(models.Model):
    parent = models.ForeignKey(News, verbose_name=_("News"), related_name="images")
    image = models.ImageField(_("Image"), max_length=250, upload_to='images')


class StaticPage(BasicContent):
    slug = models.SlugField(_("Slug"), blank=True)

    objects = ActiveObjectsManager()

    home_slug = ''

    @permalink
    def get_absolute_url(self):
        return ('home', None, dict()) if self.slug == self.home_slug else ('static_page', None, dict(slug=self.slug))


class StaticPageImage(models.Model):
    parent = models.ForeignKey(StaticPage, verbose_name=_("Static Page"), related_name="images")
    image = models.ImageField(_("Image"), max_length=250, upload_to='images')
