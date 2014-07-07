# coding=utf-8
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from feincms.admin.tree_editor import TreeEditor, ajax_editable_boolean
from .models import Category, CategoryImage, CategoryFile, PositionGroup, Position
from sorl.thumbnail.admin import AdminImageMixin


class CategoryImageInline(admin.TabularInline):
    model = CategoryImage


class CategoryFileInline(admin.TabularInline):
    model = CategoryFile


class CategoryPositionInline(admin.TabularInline):
    model = Position


class CategoryAdmin(AdminImageMixin, TreeEditor):
    list_display = 'title', 'active_toggle',
    list_per_page = 500
    search_fields = 'title', 'code', 'desc'
    active_toggle = ajax_editable_boolean('active', _('active'))
    inlines = [CategoryImageInline, CategoryFileInline, CategoryPositionInline]

admin.site.register(Category, CategoryAdmin)


class PositionGroupAdmin(admin.ModelAdmin):
    list_display = 'title',
    search_fields = 'title', 'desc'

admin.site.register(PositionGroup, PositionGroupAdmin)
