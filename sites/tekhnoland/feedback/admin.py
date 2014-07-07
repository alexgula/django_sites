# coding=utf-8

from django.contrib import admin
from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = 'category', 'name', 'email', 'post_date',
    search_fields = 'text', 'name', 'email',
    date_hierarchy = 'post_date'
    list_filter = 'category', 'post_date',

admin.site.register(Feedback, FeedbackAdmin)
