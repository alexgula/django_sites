# coding=utf-8
from collections import OrderedDict
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeForeignKey, TreeManyToManyField
from mptt.models import MPTTModel, TreeManager
from django_extensions.db.fields import UUIDField
from picassoft.utils.funcutils import cached
from picassoft.utils.itertools import build_object_tree


class CategoryManager(TreeManager):

    @staticmethod
    def category_parents(cat):
        if not cat.is_leaf_node() or cat.parent_id is None:
            return cat.parent_id
        return [cat.parent_id] + [p.id for p in cat.more_parents.all()]


    @cached('category_tree')
    def tree(self):
        categories = self.get_query_set().filter(active=True).all().prefetch_related('more_parents')

        return build_object_tree(categories,
                                 lambda cat: cat.pk,
                                 lambda cat: CategoryManager.category_parents(cat),
                                 lambda cat: dict(title=cat.title, url=cat.get_absolute_url()))


class Category(MPTTModel):
    title = models.CharField(_("Title"), max_length=250)
    code = models.CharField(_("Code"), max_length=250, blank=True)
    logo = models.ImageField(_("Logo"), max_length=250, upload_to='images', blank=True)
    desc = models.TextField(_("Description"), blank=True)
    created_on = models.DateTimeField(_("Created On"), auto_now_add=True)
    active = models.BooleanField(_("Active"), default=True)
    parent = TreeForeignKey('self', verbose_name=_("Parent"), null=True, blank=True, related_name='children')
    more_parents = TreeManyToManyField('self', verbose_name=_("Additional Parents"),
                                       null=True, blank=True, related_name='more_children', symmetrical=False)
    interop_id = UUIDField(_("1C id"), blank=True)

    objects = CategoryManager()

    @property
    def position_groups(self):
        """Group positions by their group, keeping group order. Only groups that have positions are returned.

        :return: List of tuples (position group, group positions).
        """
        groups = OrderedDict()
        for position in self.positions.all():
            if position.group.id in groups:
                group, positions = groups[position.group.id]
                positions.append(position)
            else:
                groups[position.group.id] = position.group, [position]
        return groups.values()

    def __unicode__(self):
        return self.title

    def get_text(self):
        return u"{0}{1}{2}".format(self.title, self.code, self.desc)

    @permalink
    def get_absolute_url(self):
        return 'category_detail', None, dict(pk=self.pk)


class CategoryImage(models.Model):
    category = TreeForeignKey(Category, verbose_name=_("Category"), related_name="images")
    image = models.ImageField(_("Image"), max_length=250, upload_to='images')
    caption = models.CharField(_("Caption"), max_length=250, blank=True)

    def __unicode__(self):
        return self.caption


class CategoryFile(models.Model):
    category = TreeForeignKey(Category, verbose_name=_("Category"), related_name="files")
    file = models.FileField(_("File"), max_length=250, upload_to='files')
    caption = models.CharField(_("Caption"), max_length=250, blank=True)

    def __unicode__(self):
        return self.caption


class PositionGroup(models.Model):
    title = models.CharField(_("Title"), max_length=250)

    def __unicode__(self):
        return self.title


class Position(models.Model):
    category = TreeForeignKey(Category, verbose_name=_("Category"), related_name="positions")
    group = models.ForeignKey(PositionGroup, verbose_name=_("Group"), related_name="positions")
    order = models.PositiveIntegerField(_("Order"))
    title = models.CharField(_("Title"), max_length=250)
    desc = models.TextField(_("Description"), blank=True)

    def __unicode__(self):
        return self.title
