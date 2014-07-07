from django.contrib import admin
from .models import Slide

class SlideAdmin(admin.ModelAdmin):
    list_display = 'title', 'active', 'position'
    list_filter = 'active',
    ordering = 'position',
    list_editable = 'active', 'position',

admin.site.register(Slide, SlideAdmin)
