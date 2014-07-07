# coding=utf-8
from django.contrib import admin
from .models import Author, Contest, Photo


class AuthorAdmin(admin.ModelAdmin):
    search_fields = 'email', 'name',
    list_display = 'active', 'email', 'name', 'phone',
    list_editable = 'active',
    list_display_links = 'email', 'name', 'phone',
    exclude = 'password', 'activation_key', 'activated'

admin.site.register(Author, AuthorAdmin)


class ContestAdmin(admin.ModelAdmin):
    pass

admin.site.register(Contest, ContestAdmin)


class PhotoAdmin(admin.ModelAdmin):
    list_display = 'name', 'author', 'post_date', 'votes', 'active',
    list_editable = 'votes', 'active',
    list_filter = 'contest', 'author'
    date_hierarchy = 'post_date'

admin.site.register(Photo, PhotoAdmin)
