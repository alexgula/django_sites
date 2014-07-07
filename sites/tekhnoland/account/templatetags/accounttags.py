# coding=utf-8
from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def login_next_url(context):
    request_path = context['request'].get_full_path()
    logout_url = reverse('admin:logout')
    complete_url = reverse('account:register_complete')
    return request_path if not logout_url in request_path and not complete_url in request_path else reverse('home')
