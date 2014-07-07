# coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Feedback(models.Model):
    topic = models.CharField(_(u"Topic"), max_length=250)
    name = models.CharField(_(u"Name"), max_length=100)
    phone = models.CharField(_(u"Phone"), max_length=25)
    city = models.CharField(_(u"City"), max_length=50)
    email = models.EmailField(_(u"Email"))
    text = models.TextField(_(u"Message text"))
    post_date = models.DateTimeField(_(u"Post date"), auto_now_add=True)

    class Meta:
        ordering = '-post_date',
