from django.contrib import admin
from .models import OneNew, Photo
from sorl.thumbnail.admin import AdminImageMixin

class PhotosInline(AdminImageMixin, admin.StackedInline):
    model = Photo

class NewsAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = 'published_date', 'title'
    inlines = [PhotosInline]

admin.site.register(OneNew,NewsAdmin)
admin.site.register(Photo)
