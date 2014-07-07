# coding=utf-8
from django import template
from django.template.loader import render_to_string
from ..models import Poll, Answer, Choice

register = template.Library()

@register.simple_tag(takes_context=True)
def poll(context):
    user = context['request'].user
    if not user.is_authenticated():
        return u""

    try:
        poll = Poll.objects.filter(active=True).order_by('-create_date')[0]
    except IndexError:
        return u""

    try:
        Answer.objects.get(poll=poll, customer=user)
        template_name = 'polls/polls_result.html'
    except Answer.DoesNotExist:
        template_name = 'polls/polls_questions.html'

    return render_to_string(template_name, {
        'poll': poll,
        'csrf_token': context['csrf_token'],
        'next': context['request'].get_full_path(),
    })
