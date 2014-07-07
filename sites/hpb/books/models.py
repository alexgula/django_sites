from picassoft.utils.templatetags.markup import restructuredtext
from django.db import models
from localeurl.models import reverse
from sorl.thumbnail import ImageField
from ..rstutil.validators import validate_rst

# Create your models here.
class Book(models.Model):
    slug = models.SlugField(max_length=150)
    author = models.CharField(max_length=150)
    title = models.CharField(max_length=200)
    preamble = models.TextField(blank=True, validators=[validate_rst])
    text = models.TextField(blank=True, validators=[validate_rst])
    cover = ImageField(upload_to='photos', blank=True)
    file_pdf = models.FileField(upload_to='files_pdf', blank=True, null=True)

    def __unicode__(self):
        return u'%s - %s' % (self.author.upper(), self.title)

    def get_absolute_url(self):
        return reverse('book_details', kwargs=dict(book_slug=self.slug, page_num=1))

    class Meta:
        ordering = ('author', 'title' )

class Part(models.Model):
    in_book = models.ForeignKey(Book)
    slug = models.SlugField(max_length=150)
    page_num = models.IntegerField()
    level = models.IntegerField()
    order = models.IntegerField()
    title = models.CharField(max_length=200,blank=True)
    text = models.TextField(blank=True, validators=[validate_rst])
    text_html = models.TextField(blank=True)

    class Meta:
        ordering = ('in_book', 'page_num', 'order' )

    def __unicode__(self):
        return u"{}-{}".format(self.page_num, self.title)

    def save(self, *args, **kwargs):
        self.text_html = restructuredtext(self.text)
        super(Part, self).save(*args, **kwargs)
