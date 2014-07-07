# coding=utf-8
from picassoft.utils.views import permalink
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.utils.safestring import mark_safe
from picassoft.utils.templatetags.markup import restructuredtext
from mptt.models import MPTTModel, TreeForeignKey
from sorl.thumbnail.shortcuts import get_thumbnail
from sorl.thumbnail import ImageField
from feincms.models import create_base_model


POSITION_CHOICES = (
    ('right', _("Right")),
    ('center', _("Center")),
    ('left', _("Left")),
)

# Just for extracting locales
pgettext_lazy('singular', "News")
pgettext_lazy('plural', "News")

IMAGE_TEMPLATE = u"""
    <div class='image-{position} image-content' style='width: {thumb.width}px;'>
        <a rel='colorbox' href='{image.url}' title='{caption}'>
            <img src='{thumb.url}' width='{thumb.width}' height='{thumb.height}' alt='{caption}'/>
        </a>
        {div_caption}
    </div>
"""

IMAGE_CAPTION_TEMPLATE = u"<div class='image-caption'>{caption}</div>"

class ImageContent(models.Model):

    image = ImageField(_("Image"), upload_to='images', max_length=250)
    caption = models.CharField(_("Caption"), max_length=250, blank=True)

    class Meta:
        abstract = True
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def _render(self, thumb_conf_name, full_conf_name):
        conf = settings.THUMBNAIL_SETTINGS
        thumb_conf = conf[thumb_conf_name]
        full_conf = conf[full_conf_name]
        thumb = get_thumbnail(self.image, thumb_conf[0], **thumb_conf[1])
        image = get_thumbnail(self.image, full_conf[0], **full_conf[1])
        div_caption = IMAGE_CAPTION_TEMPLATE.format(caption=self.caption) if self.caption else u""
        tag = IMAGE_TEMPLATE.format(image=image, thumb=thumb, position=self.position, caption=self.caption, div_caption=div_caption)
        return mark_safe(tag)

    def render(self, **kwargs):
        return self._render('PAGE_IMAGE', 'FULLSCREEN')

    def render_condensed(self, **kwargs):
        return self._render('PAGE_IMAGE_CONDENSED', 'FULLSCREEN')

    @classmethod
    def initialize_type(cls, positions=None):
        if positions is None:
            positions = POSITION_CHOICES

        position = models.CharField(_("Position"), max_length=10, choices=positions, default=positions[0][0])
        position.contribute_to_class(cls, 'position')


class RestructuredContent(models.Model):
    """Content type which can be used to input RestructuredText into the CMS."""

    text = models.TextField(_("content"), blank=True)

    class Meta:
        abstract = True
        verbose_name = _("Structured text")
        verbose_name_plural = _("Structured texts")

    def render(self, **kwargs):
        return restructuredtext(self.text)


class HtmlContent(models.Model):
    """Content type which can be used to input plain HTML into the CMS."""

    text = models.TextField(_("content"), blank=True)

    class Meta:
        abstract = True
        verbose_name = _("HTML text")
        verbose_name_plural = _("HTML texts")

    def render(self, **kwargs):
        return mark_safe(self.text)


class TitleMixin(object):

    def __unicode__(self):
        return self.title


class News(create_base_model(), TitleMixin):
    title = models.CharField(_("Title"), max_length=250)
    text = models.TextField(_("Text"), blank=True)
    image = ImageField(_("Image"), upload_to='images', max_length=250, blank=True)
    pub_date = models.DateTimeField(_("Publication Date"), auto_now_add=True)
    active = models.BooleanField(_("Active"), default=True)

    class Meta():
        verbose_name = _("News")
        verbose_name_plural = _("News")
        ordering = ['-pub_date']

    @permalink
    def get_absolute_url(self):
        return 'news_detail', None, {'pk': self.pk}


class InfoPage(create_base_model(MPTTModel), TitleMixin):
    """Information page for the left menu."""
    title = models.CharField(_("Title"), max_length=250)
    text = models.TextField(_("Text"), blank=True)
    image = ImageField(_("Image"), upload_to='images', max_length=250, blank=True)
    slug = models.SlugField(_("Slug"), unique=True)
    parent = TreeForeignKey('self', verbose_name=_("Parent"), null=True, blank=True, related_name='children')
    active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Information Page")
        verbose_name_plural = _("Information Pages")

    @permalink
    def get_absolute_url(self):
        return 'info_detail', None, {'slug': self.slug}


class GalleryPage(create_base_model(MPTTModel), TitleMixin):
    """Gallery page."""
    title = models.CharField(_("Title"), max_length=250)
    text = models.TextField(_("Text"), blank=True)
    image = ImageField(_("Image"), upload_to='images', max_length=250, blank=True)
    slug = models.SlugField(_("Slug"), unique=True)
    parent = TreeForeignKey('self', verbose_name=_("Parent"), null=True, blank=True, related_name='children')
    active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Gallery Page")
        verbose_name_plural = _("Gallery Pages")
        ordering = ['title']

    @permalink
    def get_absolute_url(self):
        return 'gallery_detail', None, {'slug': self.slug}
