# coding=utf-8
from django.db import models
from django.http import QueryDict
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from ..mediatools import image_variants
from ..mediatools.models import ImageFieldManaged
from picassoft.utils.validators import validate_percent
from picassoft.utils.views import permalink
from ..ratings.models import RatedModel
from ..auction.models import Lot, PercentStepBidCalculator, FixedStepBidValidator


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True)
    desc = models.TextField(_("Description"), blank=True)
    weight = models.SmallIntegerField(_("Weight"), blank=True, null=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['weight', 'name']

    def __unicode__(self):
        return self.name


class Term(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True)
    category = models.ForeignKey(Category, verbose_name=_("Category"))
    abbr = models.CharField(_("Abbreviation"), max_length=100, blank=True)
    weight = models.SmallIntegerField(_("Weight"), blank=True, null=True)

    class Meta:
        verbose_name = _("Term")
        verbose_name_plural = _("Terms")
        ordering = ['weight', 'name']

    def __unicode__(self):
        return u"{0} | {1}".format(self.category.__unicode__(), self.name)

    def save(self, *args, **kwargs):
        super(Term, self).save(*args, **kwargs) # Call the "real" save() method.
        FacetModel.save_objects(FacetModel.objects.filter(terms=self))


class FacetModel(models.Model):
    terms = models.ManyToManyField(Term, verbose_name=_("Terms"))
    filter = models.TextField(_("Filter"), blank=True)

    class Meta:
        verbose_name = _("Facet model")
        verbose_name_plural = _("Facet models")

    def save(self, *args, **kwargs):
        # If new object, save first to initialize id
        if not self.id:
            super(FacetModel, self).save(*args, **kwargs)

        # Call the base save() method if the filter has been updated.
        self.update_filter()
        super(FacetModel, self).save(*args, **kwargs)

    def update_filter(self):
        self.filter = self.filter_dict.urlencode()

    @property
    def filter_dict(self):
        dict = QueryDict(u"", mutable=True)
        terms = [(term.category.slug, term.slug) for term in self.terms.all()]
        for key, value in terms:
            dict.appendlist(key, value)
        return dict

    def term_abbrs(self):
        return [term.abbr for term in self.terms.order_by('category__weight').all() if term.abbr]

    def __unicode__(self):
        return self.filter

    @permalink
    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return ('admin:%s_%s_change' % (content_type.app_label, content_type.model), (self.id,))

    @staticmethod
    def save_objects(queryset):
        """Save all objects in the queryset.

        Usually used for updating filters for all models linked to the specified model.
        """
        for obj in queryset:
            obj.save()


class Author(FacetModel):
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True)
    desc = models.CharField(_("Description"), max_length=1000)
    date_birth = models.DateField(_("Birth date"))
    date_death = models.DateField(_("Death date"))
    contemporaries = models.ManyToManyField('self', verbose_name=_("Contemporaries"), through='AuthorContemporary', symmetrical=False, blank=True)
    portrait = ImageFieldManaged(_("Portrait"), field_name='portrait')
    sign = ImageFieldManaged(_("Sign"), field_name='sign')
    is_listed = models.BooleanField(_("Listed"), default=True, db_index=True)

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

    def file_name_builder(self, field_name):
        """
        Build file name parts for the field name. The last path must be without extension (will be added automatically)

        Examples:
          ('zaretsky', 'portrait')
          ('zaretsky', 'sign')
        """
        return self.slug, field_name.lower()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Author, self).save(*args, **kwargs)

        FacetModel.save_objects(Work.objects.filter(author=self))

    @property
    def filter_dict(self):
        dict = super(Author, self).filter_dict
        periods = self.lifeperiod_set.all()
        for period in periods:
            dict.appendlist('period', period.slug)
        return dict

    @permalink
    def get_absolute_url(self):
        return ('catalogue_author_detail', (), {
            'author_slug': self.slug})


class ContemporaryType(models.Model):
    name = models.CharField(_("Name"), max_length=100)

    class Meta:
        verbose_name = _("Contemporary type")
        verbose_name_plural = _("Contemporary types")

    def __unicode__(self):
        return self.name


class AuthorContemporary(models.Model):
    person = models.ForeignKey(Author, verbose_name=_("Self person"), related_name='person')
    linked = models.ForeignKey(Author, verbose_name=_("Linked person"), related_name='linked')
    weight = models.SmallIntegerField(_("Weight"))
    type = models.ForeignKey(ContemporaryType, verbose_name=_("Contemporary type"))

    class Meta:
        verbose_name = _("Author contemporary")
        verbose_name_plural = _("Author contemporaries")

    def __unicode__(self):
        return u"{0} - {1}".format(self.person.__unicode__(), self.linked.__unicode__())


class LifePeriod(models.Model):
    author = models.ForeignKey(Author, verbose_name=_("Author"))
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"), )
    year_begin = models.SmallIntegerField(_("Start year"), blank=True, null=True)
    year_end = models.SmallIntegerField(_("End year"), blank=True, null=True)
    bio = models.TextField(_("Biography"), blank=True)

    class Meta:
        verbose_name = _("Life period")
        verbose_name_plural = _("Life periods")

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(LifePeriod, self).save(*args, **kwargs) # Call the "real" save() method.
        FacetModel.save_objects(Work.objects.filter(periods=self))


class Owner(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    desc = models.CharField(_("Description"), max_length=1000, blank=True)

    class Meta:
        verbose_name = _("Owner")
        verbose_name_plural = _("Owners")


class TopManager(models.Manager):

    def top(self, count=10):
        qs = self.get_query_set().filter(is_listed=True).order_by('-rating_votes')
        return qs[:count]


class Work(FacetModel, RatedModel):
    author = models.ForeignKey(Author, verbose_name=_("Author"))
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"), )
    desc = models.TextField(_("Description"), blank=True)
    years = models.CharField(_("Creation years"), max_length=100, blank=True, null=True)
    height = models.CharField(_("Height"), max_length=100, blank=True, null=True)
    width = models.CharField(_("Width"), max_length=100, blank=True, null=True)
    pub_date = models.DateTimeField(_("Publication date"), auto_now_add=True)
    periods = models.ManyToManyField(LifePeriod, verbose_name=_("Life periods"), blank=True)#, limit_choices_to={'author__slug': author.slug})
    image = ImageFieldManaged(_("Image"), field_name='original', blank=True)
    owner = models.ForeignKey(Owner, verbose_name=_("Owner"), blank=True, null=True)
    image_offset_h = models.IntegerField(_("Horizontal offset (+/-100%)"), default=0, validators=[validate_percent])
    image_offset_v = models.IntegerField(_("Vertical offset (+/-100%)"), default=0, validators=[validate_percent])
    is_listed = models.BooleanField(_("Listed"), default=True, db_index=True)

    objects = TopManager()

    class Meta:
        verbose_name = _("Work")
        verbose_name_plural = _("Works")
        unique_together = ('author', 'slug', )
        ordering = ['-rating_value', '-pub_date', '-id']

    def file_name_builder(self, field_name):
        """
        Examples:
          ('zaretsky', 'image', '123')
          ('zaretsky', 'dzi', '123')
        """
        return self.author.slug, field_name.lower(), self.slug

    def __unicode__(self):
        return self.name

    def dzi(self, overwrite=False):
        return image_variants.load_field_dzi(self.image, overwrite=overwrite)

    def thumbnail(self, overwrite=False):
        return image_variants.load_field_thumbnail(self.image, overwrite=overwrite, size=150, fill=True, offset_h=self.image_offset_h, offset_v=self.image_offset_v)

    def preview(self, overwrite=False):
        return image_variants.load_field_thumbnail(self.image, overwrite=overwrite, size=340, fill=True, offset_h=self.image_offset_h, offset_v=self.image_offset_v)

    def image_variants(self, overwrite=False):
        return (self.dzi(overwrite), self.thumbnail(overwrite), self.preview(overwrite))

    def size(self):
        return u"x".join(filter(None, (self.height, self.width)))

    def short_desc(self):
        return filter(None, [self.size(), self.years])

    @permalink
    def get_absolute_url(self):
        return ('catalogue_work_detail', (), {
            'author_slug': self.author.slug, 'work_slug': self.slug})

    def build_filter_set(self):
        author = (u"author", self.author.slug)
        periods = [(u"period", period.slug) for period in self.periods.all()]
        return [author] + periods + super(Work, self).build_filter_set()

    def save(self, *args, **kwargs):
        super(Work, self).save(*args, **kwargs) # Call the "real" save() method.

    @property
    def filter_dict(self):
        dict = super(Work, self).filter_dict
        periods = self.periods.all()
        for period in periods:
            dict.appendlist('period', period.slug)
        return dict


class Deal(models.Model):
    work = models.ForeignKey(Work, verbose_name=_("Work"))
    date = models.DateField(_("Deal date"), blank=True, null=True)
    seller = models.ForeignKey(Owner, verbose_name=_("Seller"), related_name='seller', blank=True, null=True)
    buyer = models.ForeignKey(Owner, verbose_name=_("Buyer"), related_name='buyer', blank=True, null=True)
    price = models.IntegerField(_("Sell price"), blank=True, null=True)
    desc = models.TextField(_("Description"), blank=True)

    class Meta:
        verbose_name = _("Deal")
        verbose_name_plural = _("Deals")


class WorkLot(Lot, PercentStepBidCalculator, FixedStepBidValidator):
    work = models.ForeignKey(Work, verbose_name=_("Work"))

    def __unicode__(self):
        return u"{} - {}".format(self.work, self.start_date)

    @permalink
    def get_absolute_url(self):
        return ('catalogue_work_detail', (), {
            'author_slug': self.work.author.slug, 'work_slug': self.work.slug})
