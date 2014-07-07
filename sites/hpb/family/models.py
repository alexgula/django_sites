from django.db import models
from localeurl.models import reverse
from sorl.thumbnail import ImageField
from ..rstutil.validators import validate_rst


class FamilyMember(models.Model):
    birth_date = models.CharField(max_length=30)
    died_date = models.CharField(max_length=30, blank=True)
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=20)
    father_name = models.CharField(max_length=20, blank=True)
    preview = models.TextField()
    citation = models.TextField(blank=True)
    autor_of_citation = models.CharField(max_length=20, blank=True)
    text = models.TextField(validators=[validate_rst])
    main_portrait = ImageField(upload_to='photos', blank=True)
    title_for_main_portrait = models.CharField(max_length=150)

    def __unicode__(self):
        return u'%s %s %s' % (self.surname, self.name, self.father_name)

    def get_absolute_url(self):
        return reverse('family_member_details', kwargs=dict(member_id=self.id))

    class Meta:
        ordering = ('surname', )


class Picture(models.Model):
    member = models.ForeignKey(FamilyMember)
    title = models.CharField(max_length=150)
    image = ImageField(upload_to='photos',blank=True)

    def __unicode__(self):
        return self.title


class Gallery(models.Model):
    title = models.CharField(max_length=150)
    image = ImageField(upload_to='photos',blank=True)

    def __unicode__(self):
        return self.title
