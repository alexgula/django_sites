# coding=utf-8
from django import template
from ..models import Author, Work

register = template.Library()


@register.inclusion_tag('library/block_author_list.html')
def popular_authors(count):
    author_list = Author.objects.listed().prefetch_related('work_set')[:count]
    return dict(author_list=author_list)


@register.inclusion_tag('library/block_work_list.html')
def popular_works(count):
    work_list = Work.objects.listed()[:count]
    return dict(work_list=work_list)
