# coding=utf-8
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField


class News(models.Model):
    title = models.CharField(_("Title"), max_length=250)
    text = models.TextField(_("Text"), blank=True)
    image = ImageField(_("Image"), upload_to='images', max_length=250, blank=True)
    pub_date = models.DateTimeField(_("Publication Date"), auto_now_add=True)
    active = models.BooleanField(_("Active"), default=True)

    class Meta():
        verbose_name = _("News")
        verbose_name_plural = _("Newses")
        ordering = ['-pub_date']

    def __unicode__(self):
        return u" ".join([self.pub_date.strftime('%Y-%m-%d'), self.title])

    @permalink
    def get_absolute_url(self):
        return 'news:detail', None, {'pk': self.pk}
