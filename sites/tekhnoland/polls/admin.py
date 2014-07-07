from django.contrib import admin
from .models import Choice, Poll, Answer


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class PollAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = 'question', 'active'
    list_filter = 'active',
    search_fields = 'question',
    date_hierarchy = 'create_date'

admin.site.register(Poll, PollAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_filter = 'poll',

admin.site.register(Answer, AnswerAdmin)
