from django.db import models
from localeurl.models import reverse
from sorl.thumbnail import ImageField

class OneNew(models.Model):
    title = models.CharField(max_length=200)
    published_date = models.DateField()
    preview = models.TextField(blank=True)
    text = models.TextField()
    main_picture = ImageField(upload_to='photos', blank=True)
    title_for_main_picture =  models.CharField(max_length=150, blank=True)

    def __unicode__(self):
        return u"{}-{}".format(self.published_date.strftime(u'%Y-%m-%d'), self.title)

    def get_absolute_url(self):
        return reverse('news_details', kwargs=dict(news_id=self.id))

    class Meta:
        ordering = ('-published_date', )
        verbose_name_plural = 'OneNew'

class Photo(models.Model):
    news = models.ForeignKey(OneNew)
    title =  models.CharField(max_length=150, blank=True)
    image = ImageField(upload_to='photos', blank=True)

    def __unicode__(self):
        return u'%s' % self.title

    #def get_absolute_url(self):
    #    return reverse('photo_details', kwargs=dict(photo_id=self.id))

    class Meta:
        ordering = ('-title', )