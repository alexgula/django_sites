# coding=utf-8

from django import template

from ..models import Slide

register = template.Library()


@register.inclusion_tag('slideshow.html')
def slideshow():
    slides = Slide.objects.active()
    return dict(slides=slides)
