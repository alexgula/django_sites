# coding=utf-8

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class Currency(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    code = models.CharField(_("Code"), max_length=3, unique=True)
    lang = models.CharField(_("Language"), max_length=5, choices=settings.LANGUAGES, unique=True)
    rate = models.DecimalField(_("Rate"), max_digits=14, decimal_places=2)
