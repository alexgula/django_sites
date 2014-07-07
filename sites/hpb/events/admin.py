from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin
from .models import Event

class EventAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = 'title', 'start_date', 'end_date',
    list_editable = 'start_date', 'end_date',

admin.site.register(Event,EventAdmin)