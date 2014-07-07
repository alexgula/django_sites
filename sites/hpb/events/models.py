# coding=utf-8
from django.db import models
from localeurl.models import reverse
from sorl.thumbnail import ImageField
from ..rstutil.validators import validate_rst


class Event(models.Model):
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    title = models.CharField(max_length=200)
    preview = models.TextField(blank=True)
    text = models.TextField(blank=True, validators=[validate_rst])
    picture = ImageField(upload_to='photos',blank=True)

    def get_absolute_url(self):
        return reverse('event_details', kwargs=dict(event_id=self.id))

    class Meta:
        ordering = ('-start_date', )

    def __unicode__(self):
        #return u"{}-{:0=2}-{:0=2}-{}".format(self.start_date.year, self.start_date.month, self.start_date.day, self.title)
        #0 - заполнитель
        #= - выравниватель, т.е. что нолики дописывать слева
        #2 - количество позицый, которые выделяем под поле
        return u"{}-{}".format(self.start_date.strftime(u'%Y-%m-%d'), self.title)
