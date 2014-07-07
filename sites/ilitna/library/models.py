# coding=utf-8
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from mptt.models import MPTTModel, TreeForeignKey, TreeManager
from sorl.thumbnail import ImageField
from feincms.models import create_base_model
from . import isbn
from picassoft.utils.format import abbrev

def validate_isbn(val):
    return isbn.isValid(val)

def set_field(obj, field, value):
    """Set field of the object from the value.

    Return True if value was different from field value, False otherwise."""
    updated = False
    if getattr(obj, field) <> value:
        setattr(obj, field, value)
        updated = True
    return updated

LANGUAGES = (
    ('uk', _("Ukrainian")),
    ('ru', _("Russian")),
    ('en', _("English")),
)


class ActiveListedManager(object):

    use_for_related_fields = True

    def active(self):
        return self.get_query_set().filter(active=True)

    def listed(self):
        return self.active().filter(listed=True)


class AuthorManager(models.Manager, ActiveListedManager):
    pass


class WorkManager(TreeManager, ActiveListedManager):
    pass


class Author(models.Model):
    slug = models.SlugField(_("Slug"), unique=True)
    first_name = models.CharField(_("First Name"), max_length=100)
    family_name = models.CharField(_("Family Name"), max_length=50)
    date_born = models.CharField(_("Date of birth"), max_length=50, blank=True)
    date_died = models.CharField(_("Date of death"), max_length=50, blank=True)
    portrait = ImageField(_("Portrait"), upload_to='portrait', blank=True)
    active = models.BooleanField(_("Active"), default=True)
    listed = models.BooleanField(_("Show in List"), default=False)

    objects = AuthorManager()

    @property
    def name(self):
        return u" ".join([self.family_name, abbrev(self.first_name)])

    @property
    def full_name(self):
        return u" ".join([self.family_name, self.first_name])

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return 'library:author_detail', None, {'slug': self.slug}

    def listed_works(self):
        return self.work_set.listed()


class Work(create_base_model(MPTTModel)):
    slug = models.SlugField(_("Slug"))
    lang = models.CharField(_("Language"), max_length=5, choices=LANGUAGES)
    authors = models.ManyToManyField(Author, verbose_name=_("Authors"))
    title = models.CharField(_("Title"), max_length=250)
    teaser = models.TextField(_("Teaser"), blank=True)
    cover = ImageField(_("Cover"), upload_to='cover', blank=True)
    parent = TreeForeignKey('self', verbose_name=_("Parent"), null=True, blank=True, related_name='children')
    active = models.BooleanField(_("Active"), default=True)
    listed = models.BooleanField(_("Show in List"), default=False)
    slug_trail = models.SlugField(_("Slug Trail"), max_length=250, blank=True)

    objects = WorkManager()

    class Meta:
        verbose_name = _("Work")
        verbose_name_plural = _("Works")
        unique_together = 'slug', 'parent',

    def __unicode__(self):
        return u"{}".format(self.title)

    @permalink
    def get_absolute_url(self):
        return 'library:work_detail', None, {'slug': self.slug_trail}

    def set_slug_trail(self):
        trail = list(self.get_ancestors()) + [self]
        slug = u'/'.join(ancestor.slug for ancestor in trail)
        return set_field(self, 'slug_trail', slug)

    @property
    def present_cover(self):
        """Get first filled cover in the ancestry list."""
        if self.cover:
            return self.cover
        for parent in self.get_ancestors(ascending=True):
            if parent.cover:
                return parent.cover
        return None

@receiver(post_save, sender=Work)
def update_work(sender, instance, raw, **kwargs):
    if not raw and instance.set_slug_trail(): # Check for changes to avoid infinite recursion
        instance._mptt_meta.update_mptt_cached_fields(instance)
        instance.save()
        for child in instance.get_children(): # Children, not descendants, because signal will be sent recursively
            child.save() # Indirect recursive signal sending


class Publisher(models.Model):
    slug = models.SlugField(_("Slug"), unique=True)
    name = models.CharField(_("Name"), max_length=100)

    class Meta:
        verbose_name = _("Publisher")
        verbose_name_plural = _("Publishers")

    def __unicode__(self):
        return u"{}".format(self.name)

    @permalink
    def get_absolute_url(self):
        return 'library:publisher_detail', None, {'slug': self.slug}


class Publication(models.Model):
    isbn = models.CharField(_("ISBN Code"), max_length=13, validators=[validate_isbn], unique=True)
    work = models.ForeignKey(Work, verbose_name=_("Work"))
    publisher = models.ForeignKey(Publisher, verbose_name=_("Publisher"))
    year = models.PositiveIntegerField(_("Publication Year"))
    cover = ImageField(_("Cover"), upload_to='cover', blank=True)
    pages = models.PositiveIntegerField(_("Page count"), blank=True, null=True)
    format = models.CharField(_("Format"), max_length=50, blank=True)
    copies = models.PositiveIntegerField(_("Copies"), blank=True)
    active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Publication")
        verbose_name_plural = _("Publications")

    def __unicode__(self):
        return u"{} ({}, {})".format(self.work, self.year, self.publisher)

    @permalink
    def get_absolute_url(self):
        return 'library:publication_detail', None, {'isbn': self.isbn}

    def save(self, *args, **kwargs):
        self.isbn = isbn.isbn_strip(self.isbn)
        return super(Publication, self).save(*args, **kwargs)
