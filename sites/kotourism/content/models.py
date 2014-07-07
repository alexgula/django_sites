# coding=utf-8
import os, uuid

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from sorl.thumbnail.shortcuts import get_thumbnail

from picassoft.utils.templatetags.markup import restructuredtext

from ..managedimage.models import model_class_path, upload_path
from ..places.models import Place
from ..search.util import TranslatedUnicode


POSITION_CHOICES=(
    ('left', _("Left (1 column)")),
    ('center', _("Center (1.5 column)")),
    ('block', _("Block (2 column)")),
    ('right', _("Right (1 column)")),
)


class ImageContent(models.Model):
    """Create an ImageContent like this:
        POSITION_CHOICES=(
            ('left', 'Left'),
            ('block', 'Block'),
            ('right', 'Right'),
        )
        Cls.create_content_type(ImageContent, positions=POSITION_CHOICES)
    """

    image = models.ImageField(_("Image"), max_length=250, upload_to=upload_path('{class_path}/image/{path}/{uuid}', params_extend='image_path'))

    class Meta:
        abstract = True
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def image_path(self):
        """Build image path parameters for ImageField file name resolver."""
        id = unicode(uuid.uuid4())
        params = {
            'path': id[:2],
            'uuid': id,
            'class_path': model_class_path(self.parent),
        }
        return params

    def render(self, **kwargs):
        if self.position == 'block':
            thumb_width = '390'
        elif self.position == 'center':
            thumb_width = '290'
        else:
            thumb_width = '190'
        thumb = get_thumbnail(self.image, thumb_width, upscale=False)
        image = get_thumbnail(self.image, settings.THUMBNAIL_SETTINGS['FULLSCREEN_SIZE'], upscale=False)
        tag = u"""
            <div class='image-{position}'>
                <div class='image-content' style='width: {thumb_width}px; height: {thumb_div.height}px;'>
                    <a class='colorbox' rel='content' href='{image.url}' title=''>
                        <img src='{thumb_im.url}' width='{thumb_im.width}' height='{thumb_im.height}'/>
                    </a>
                </div>
            </div>
        """
        tag = tag.format(image=image, thumb_width=thumb_width, thumb_div=thumb, thumb_im=thumb, position=self.position)
        return mark_safe(tag)

    def get_text_translations(self):
        """Concatenate all text, including localized, for search. In case of file just return nothing."""
        return None

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
        #return mark_safe(self.text)

    def get_text_translations(self):
        """Concatenate all text, including localized, for search."""
        result = TranslatedUnicode()
        result.add_field_translations(self, 'text')
        return result


class FileContent(models.Model):
    """Content type which can be used to input RestructuredText into the CMS."""

    file = models.FileField(_("file"), max_length=250, upload_to=upload_path(u'{class_path}/file/{file_name}', params_extend='file_path'))

    class Meta:
        abstract = True
        verbose_name = _("File")
        verbose_name_plural = _("Files")

    def file_path(self):
        """Build file path parameters for FileField file name resolver."""
        params = {
            'class_path': model_class_path(self.parent),
        }
        return params

    def render(self, **kwargs):
        tag = u"""
            <div class='file'>
                <a href='{file_url}'>{file_name}</a>
            </div>
        """
        file_name = os.path.basename(self.file.name)
        tag = tag.format(file_url=self.file.url, file_name=file_name)
        return mark_safe(tag)

    def get_text_translations(self):
        """Concatenate all text, including localized, for search. In case of file just return nothing."""
        return None


class PlaceContent(models.Model):
    """Content type which can be used to input RestructuredText into the CMS."""

    place = models.ForeignKey(Place, verbose_name=_("content"), blank=True)

    class Meta:
        abstract = True
        verbose_name = _("Place link")
        verbose_name_plural = _("Place links")

    def render(self, **kwargs):
        desc = u"<br/>".join([self.place.address, self.place.phone])
        tag = u"""
            <div class='place'>
                <div class='place-title'>{name}</div>
                <div class='place-desc'>{name}</div>
            </div>
        """.format(name=self.place.name, desc=desc)
        return mark_safe(tag)
