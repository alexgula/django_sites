# coding=utf-8
from django.contrib import admin
from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = 'name', 'phone', 'email', 'post_date',
    search_fields = 'name', 'phone', 'email', 'text',
    date_hierarchy = 'post_date'

admin.site.register(Feedback, FeedbackAdmin)
