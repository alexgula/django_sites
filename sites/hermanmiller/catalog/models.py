# coding=utf-8
from decimal import Decimal
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel, TreeManager
from constance import config
from picassoft.utils.funcutils import cached
from picassoft.utils.itertools import build_object_tree
from picassoft.utils.models import ActiveManager


class CategoryManager(TreeManager):

    @cached('category_tree')
    def tree(self):
        categories = self.get_query_set().filter(active=True).all()

        return build_object_tree(categories,
                                 lambda cat: cat.pk,
                                 lambda cat: cat.parent_id,
                                 lambda cat: dict(title=cat.title, url=cat.get_absolute_url()))


class Category(MPTTModel):
    slug = models.SlugField(_("Slug"), unique=True)
    title = models.CharField(_("Title"), max_length=250)
    meta_description = models.TextField(_("Meta Description"), blank=True)
    meta_keywords = models.TextField(_("Meta Keywords"), blank=True)
    logo = models.ImageField(_("Logo"), max_length=250, upload_to='images', blank=True)
    desc = models.TextField(_("Description"), blank=True)
    created_on = models.DateTimeField(_("Created On"), auto_now_add=True)
    active = models.BooleanField(_("Active"), default=True)
    show_on_main = models.BooleanField(_("Show On Main Page"), default=False)
    parent = TreeForeignKey('self', verbose_name=_("Parent"), null=True, blank=True, related_name='children')

    objects = CategoryManager()

    def __unicode__(self):
        return self.title

    def get_text(self):
        return u"".join([self.slug, self.title, self.meta_description, self.meta_keywords, self.desc])

    @permalink
    def get_absolute_url(self):
        return 'category_detail', None, dict(slug=self.slug)


class ProductManager(models.Manager):

    def special(self):
        return self.get_query_set().filter(special=True)


class Product(models.Model):
    slug = models.SlugField(_("Slug"), unique=True)
    title = models.CharField(_("Title"), max_length=250)
    logo = models.ImageField(_("Logo"), max_length=250, upload_to='images', blank=True)
    desc = models.TextField(_("Description"), blank=True)
    price = models.DecimalField(_("Price (EUR)"), max_digits=15, decimal_places=2)
    price_national = models.DecimalField(_("Price (UAH)"), max_digits=15, decimal_places=2, blank=True, null=True)
    category = TreeForeignKey(Category, related_name='products')
    active = models.BooleanField(_("Active"), default=True)
    special = models.BooleanField(_("Special"), default=False)
    created_on = models.DateTimeField(_("Created On"), auto_now_add=True)
    properties = models.TextField(_("Properties"), blank=True,
                                  help_text=_("Each property on separate line, divided by semicolon (e.g. Color:Red)"))

    objects = ProductManager()

    def __unicode__(self):
        return self.title

    def get_text(self):
        return u"".join([self.slug, self.title, self.desc, self.properties])

    @permalink
    def get_absolute_url(self):
        return 'product_detail', None, dict(slug=self.slug, category_slug=self.category.slug)

    @property
    def price_eur(self):
        return self.price

    @property
    def price_uah(self):
        return self.price_national or self.price * Decimal(config.CURRENCY_RATE_EUR)

    @property
    def properties_other(self):
        return ((name, value) for important, name, value in self.parse_properties() if important is False)

    @property
    def properties_main(self):
        return ((name, value) for important, name, value in self.parse_properties() if important is True)

    @property
    def review_count(self):
        return len(self.reviews.active())

    def parse_properties(self):
        for line in self.properties.splitlines():
            parsed_property = line.split(':', 1)
            if len(parsed_property) == 2:
                name, value = parsed_property[0].strip(), parsed_property[1].strip()
                if name.startswith('!'):
                    important = True
                    name = name[1:]
                else:
                    important = False
                yield important, name, value


class ProductImage(models.Model):
    product = models.ForeignKey(Product, verbose_name=_("Product"), related_name="images")
    image = models.ImageField(_("Image"), max_length=250, upload_to='images')
    caption = models.CharField(_("Caption"), max_length=250, blank=True)

    def __unicode__(self):
        return self.caption


class ProductFile(models.Model):
    product = models.ForeignKey(Product, verbose_name=_("Product"), related_name="files")
    file = models.FileField(_("File"), max_length=250, upload_to='files')
    caption = models.CharField(_("Caption"), max_length=250, blank=True)

    def __unicode__(self):
        return self.caption


class ProductReview(models.Model):
    product = models.ForeignKey(Product, verbose_name=_("Product"), related_name="reviews")
    author = models.CharField(_("Author"), max_length=50)
    email = models.EmailField(_("Email"), blank=True)
    text = models.TextField(_("Text"), blank=True)
    active = models.BooleanField(_("Active"), default=False)
    created_on = models.DateTimeField(_("Created On"), auto_now_add=True)

    objects = ActiveManager()

    def __unicode__(self):
        return self.text[:100]

    class Meta:
        ordering = ["-created_on"]
