# coding=utf-8
from django.db import models


class News(models.Model):
    post_date = models.DateTimeField(auto_now_add=True, db_index=True)
    text = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    class Meta():
        ordering = ['-post_date']
        verbose_name = u"новость"
        verbose_name_plural = u"новости"

    def __unicode__(self):
        return self.text
