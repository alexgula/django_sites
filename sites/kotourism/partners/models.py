# coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField
from ..files.storage import HashedFileSystemStorage


file_storage = HashedFileSystemStorage([2])


class Partner(models.Model):
    important = models.BooleanField(_("Important"), help_text=_("Show on main page"), default=False)
    name = models.CharField(_("Name"), max_length=150)
    url = models.URLField(_("URL"))
    banner = ImageField(_("Banner"), max_length=250, upload_to='hashimages', blank=True, storage=file_storage)
    desc = models.TextField(_("Description"), blank=True)

    def __unicode__(self):
        return self.name
