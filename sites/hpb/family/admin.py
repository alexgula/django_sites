from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin
from .models import FamilyMember, Picture, Gallery

class PicturesInline(AdminImageMixin, admin.StackedInline):
    model = Picture

class FamilyAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = 'surname', 'name', 'father_name', 'birth_date', 'died_date'
    list_editable = 'birth_date', 'died_date'
    inlines = [PicturesInline]

admin.site.register(FamilyMember, FamilyAdmin)
admin.site.register(Picture)


class GalleryAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = 'title',

admin.site.register(Gallery, GalleryAdmin)
