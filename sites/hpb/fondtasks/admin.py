# coding=utf-8
from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin
from .models import FondTask
from .models import Photo

class PhotoInline(AdminImageMixin, admin.StackedInline):
    model = Photo

class TaskAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = 'title',
    inlines = [PhotoInline]

admin.site.register(FondTask,TaskAdmin)
admin.site.register(Photo)
