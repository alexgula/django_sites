from django import template
from ..models import Slide

register = template.Library()


@register.inclusion_tag('slideshow/slideshow.html')
def slideshow():
    return {'slides': Slide.objects.filter(active=True).order_by('position')}
