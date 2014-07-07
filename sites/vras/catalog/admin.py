# coding=utf-8
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from feincms.admin.tree_editor import TreeEditor, ajax_editable_boolean
from .models import Category, CategoryImage
from sorl.thumbnail.admin import AdminImageMixin


class CategoryImageInline(admin.TabularInline):
    model = CategoryImage


class CategoryAdmin(AdminImageMixin, TreeEditor):
    list_display = 'title', 'slug', 'active_toggle',
    search_fields = 'title', 'desc'
    active_toggle = ajax_editable_boolean('active', _('active'))
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CategoryImageInline, ]

admin.site.register(Category, CategoryAdmin)
