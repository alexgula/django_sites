# coding=utf-8
from django.db import models
from picassoft.utils.templatetags.markup import restructuredtext
from django.utils.safestring import mark_safe


class RestructuredContent(models.Model):
    """Content type which can be used to input RestructuredText into the CMS."""

    text = models.TextField(blank=True)

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return restructuredtext(self.text)


class HTMLContent(models.Model):
    """Content type which can be used to input any HTML into the CMS."""

    text = models.TextField(blank=True)

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return mark_safe(self.text)
