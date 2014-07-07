# coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Log(models.Model):
    action_date = models.DateTimeField(_("Action Date"), auto_now_add=True)
    success = models.BooleanField(_("Is action successful"), default=True)
    message = models.TextField(_("Message"))
    data = models.TextField(_("Request Data"), blank=True)

    class Meta:
        ordering = ['-action_date']
