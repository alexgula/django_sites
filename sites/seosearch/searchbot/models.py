from django.db import models


class Site(models.Model):
    site_domain = models.CharField(max_length=350)
    keywords = models.TextField()

    def __unicode__(self):
        return self.site_domain


class Search(models.Model):
    date = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = '-date',

    def __unicode__(self):
        return  self.date.strftime('%Y-%m-%d %H:%M')


class Results(models.Model):
    site = models.ForeignKey(Site)
    search = models.ForeignKey(Search)
    keyword = models.CharField(max_length=150)
    engine = models.CharField(max_length=50)
    position = models.IntegerField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
