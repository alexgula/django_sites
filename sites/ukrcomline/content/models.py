# coding=utf-8
import os
from django.db import models
from django.conf import settings
from django.db.models import permalink
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from feincms.models import create_base_model

from sorl.thumbnail.shortcuts import get_thumbnail

from picassoft.utils.templatetags.markup import restructuredtext


class CreatedObjectsManager(models.Manager):
    def get_query_set(self):
        return super(CreatedObjectsManager, self).get_query_set().order_by('-created_on')

    def active(self):
        return self.get_query_set().filter(active=True)


class BasicContent(create_base_model()):
    title = models.CharField(_("Title"), max_length=250)
    logo = models.ImageField(_("Logo"), max_length=250, upload_to='images', blank=True)
    desc = models.TextField(_("Description"), blank=True)
    active = models.BooleanField(_("Active"), default=True)

    objects = CreatedObjectsManager()

    def __unicode__(self):
        return self.title

    def get_text(self):
        return u"{0}{1}".format(self.title, self.desc)

    class Meta(object):
        abstract = True


class News(BasicContent):
    created_on = models.DateTimeField(_("Created On"))

    @permalink
    def get_absolute_url(self):
        return 'news_detail', None, dict(pk=self.pk)

    class Meta(object):
        verbose_name_plural = _("News list")


class Portfolio(BasicContent):
    created_on = models.DateTimeField(_("Created On"))

    @permalink
    def get_absolute_url(self):
        return 'portfolio_detail', None, dict(pk=self.pk)


class Certificate(BasicContent):
    created_on = models.DateTimeField(_("Created On"), auto_now_add=True)

    @permalink
    def get_absolute_url(self):
        return 'certificate_detail', None, dict(pk=self.pk)


class StaticPage(BasicContent):
    created_on = models.DateTimeField(_("Created On"), auto_now_add=True)
    slug = models.SlugField(_("Slug"))

    @permalink
    def get_absolute_url(self):
        return 'static_page', None, dict(slug=self.slug)


class ImageContent(models.Model):
    image = models.ImageField(_("Image"), max_length=250, upload_to='images', blank=True)
    caption = models.CharField(_("Caption"), max_length=250, blank=True)
    url = models.URLField(_("Link"), max_length=500, blank=True)
    text = models.TextField(_("Text"), blank=True)

    class Meta(object):
        abstract = True
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def render(self, **kwargs):
        thumb = get_thumbnail(self.image, settings.THUMBNAIL_SETTINGS['CONTENT_PICTURE_NEWS'], upscale=False,
                              crop='center')
        image = get_thumbnail(self.image, settings.THUMBNAIL_SETTINGS['FULLSCREEN_SIZE'], upscale=False)
        tag = render_to_string("content/image_content.html", dict(
            image=image, thumb=thumb, caption=self.caption, url=self.url, text=self.text))
        return mark_safe(tag)


class RestructuredContent(models.Model):
    """Content type which can be used to input RestructuredText into the CMS."""
    text = models.TextField(_("Text"), blank=True)

    class Meta(object):
        abstract = True
        verbose_name = _("Structured text")
        verbose_name_plural = _("Structured texts")

    def render(self, **kwargs):
        tag = u"<div class='text'>{}</div>".format(restructuredtext(self.text))
        return mark_safe(tag)


class FileContent(models.Model):
    """Content type which can be used to input RestructuredText into the CMS."""
    file = models.FileField(_("File"), max_length=250, upload_to='files', blank=True)
    caption = models.CharField(_("Caption"), max_length=250, blank=True)

    class Meta(object):
        abstract = True
        verbose_name = _("File")
        verbose_name_plural = _("Files")

    def render(self, **kwargs):
        file_name = os.path.basename(self.file.name)
        tag = render_to_string('content/file_content.html', dict(
            file_url=self.file.url, file_name=file_name, caption=self.caption))
        return mark_safe(tag)

# Import translations to register them
# If real translations are added, remove this
from . import translations
