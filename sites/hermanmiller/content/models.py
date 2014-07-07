# coding=utf-8
import os
from django.conf import settings
from django.db import models
from django.db.models import permalink
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from feincms.models import create_base_model

from sorl.thumbnail.shortcuts import get_thumbnail

from picassoft.utils.templatetags.markup import restructuredtext

from .model_choices import POSITION_CHOICES, IMAGESIZE_CHOICES, IMAGESIZE_270, POSITION_LEFT


class ActiveObjectsManager(models.Manager):
    def active(self):
        return self.get_query_set().filter(active=True)


class CreatedObjectsManager(ActiveObjectsManager):
    def get_query_set(self):
        return super(CreatedObjectsManager, self).get_query_set().order_by('-created_on')


class BasicContent(create_base_model()):
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


class StaticPage(BasicContent):
    slug = models.SlugField(_("Slug"), blank=True)

    objects = ActiveObjectsManager()

    home_slug = ''

    @permalink
    def get_absolute_url(self):
        return ('home', None, dict()) if self.slug == self.home_slug else ('static_page', None, dict(slug=self.slug))


class ImageContent(models.Model):
    image = models.ImageField(_("Image"), max_length=250, upload_to='images')
    position = models.CharField(_("Position"), max_length=20, choices=POSITION_CHOICES, default=POSITION_LEFT)
    size = models.CharField(_("Size"), max_length=20, choices=IMAGESIZE_CHOICES, default=IMAGESIZE_270)
    caption = models.CharField(_("Caption"), max_length=250, blank=True)
    url = models.URLField(_("Link"), max_length=500, blank=True)
    text = models.TextField(_("Text"), blank=True)

    class Meta(object):
        abstract = True
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def render(self, **kwargs):
        thumb = get_thumbnail(self.image, self.size, upscale=False)
        image = get_thumbnail(self.image, settings.THUMBNAIL_SETTINGS['FULLSCREEN_SIZE'], upscale=False)
        tag = render_to_string("content/image_content.html",
                               {'image': image, 'thumb': thumb, 'position': self.position, 'size': self.size, 'caption': self.caption,
                                'url': self.url, 'text': self.text})
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
        tag = render_to_string('content/file_content.html',
                               {'file_url': self.file.url, 'file_name': file_name, 'caption': self.caption})
        return mark_safe(tag)

# Import translations to register them
# If real translations are added, remove this
from . import translations
