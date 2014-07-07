from django.db import models
from django.utils.translation import ugettext_lazy as _


class Slide(models.Model):
    image = models.ImageField(_("Image"), max_length=250, upload_to='images')
    title = models.CharField(_("Title"), max_length=250)
    position = models.PositiveIntegerField(_("Position"),default=1)
    desc = models.TextField(_("Description"), blank=True)
    gotolink = models.URLField(_("Gotolink"), max_length=250, blank=True)
    active = models.BooleanField(_("Active"), default=True)

    def __unicode__(self):
        return self.title
