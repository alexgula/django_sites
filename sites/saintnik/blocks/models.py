# coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TextBlock(models.Model):
    code = models.CharField(_("Code"), unique=True, max_length=50)
    text = models.TextField(_("Text"), blank=True)
    comment = models.TextField(_("Comment"), blank=True)

    class Meta:
        verbose_name = _("Text block")
        verbose_name_plural = _("Text blocks")
        ordering = 'code',

    def __unicode__(self):
        return self.comment
