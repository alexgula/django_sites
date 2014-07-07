from django import template
from ..models import Term

register = template.Library()

@register.inclusion_tag('catalogue/categories.html')
def show_categories():
    terms = Term.objects.select_related()
    return {'terms': terms}

@register.inclusion_tag('catalogue/filters.html', takes_context=True)
def show_filters(context):
    return {
        'filters': context['filters'],
        'search_url': context['search_url'],
    }
