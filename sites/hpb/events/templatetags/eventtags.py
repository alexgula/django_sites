from django import template
from ..models import Event

register = template.Library()

@register.inclusion_tag('latest_event_block.html')
def latest_event():
    try:
        event = Event.objects.order_by('-start_date', '-start_time')[0]
    except IndexError:
        event = None
    return {'event': event}
