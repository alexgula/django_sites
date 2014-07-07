# coding=utf-8
from django.db import models
from sorl.thumbnail import ImageField
from ..rstutil.validators import validate_rst


class FondTask(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(validators=[validate_rst])
    main_photo = ImageField(upload_to='photos',blank=True)
    title_for_main_photo = models.CharField(max_length=150,blank=True)

    def __unicode__(self):
        return u"{}".format(self.title)


class Photo(models.Model):
    task = models.ForeignKey(FondTask)
    title =  models.CharField(max_length=150, blank=True)
    image = ImageField(upload_to='photos', blank=True)

    class Meta:
        ordering = ('-title', )

    def __unicode__(self):
        return u'%s' % self.title
