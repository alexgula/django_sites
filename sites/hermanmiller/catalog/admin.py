# coding=utf-8
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from feincms.admin.tree_editor import TreeEditor, ajax_editable_boolean
from .models import Category, Product, ProductImage, ProductFile, ProductReview
from sorl.thumbnail.admin import AdminImageMixin


class CategoryAdmin(TreeEditor, AdminImageMixin):
    list_display = 'title', 'slug', 'active_toggle',
    search_fields = 'title', 'slug', 'desc'
    active_toggle = ajax_editable_boolean('active', _('active'))

admin.site.register(Category, CategoryAdmin)


class ProductImageInline(admin.TabularInline, AdminImageMixin):
    model = ProductImage


class ProductFileInline(admin.TabularInline):
    model = ProductFile


class ProductReviewInline(admin.TabularInline):
    model = ProductReview


class ProductAdmin(admin.ModelAdmin, AdminImageMixin):
    list_display = 'title', 'slug', 'active_toggle',
    search_fields = 'title', 'slug', 'desc'
    active_toggle = ajax_editable_boolean('active', _('active'))
    inlines = [ProductImageInline, ProductFileInline, ProductReviewInline]

admin.site.register(Product, ProductAdmin)
