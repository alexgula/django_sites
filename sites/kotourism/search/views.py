# coding=utf-8
from django.utils.translation import ugettext_lazy as _
from ..navigation.views import TemplateNavigationView
from ..navigation.models import StaticNode
from haystack.query import SearchQuerySet, EmptySearchQuerySet


class SearchView(TemplateNavigationView):
    template_name = 'search/search.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        query = self.request.GET.get('q', u"")
        if query:
            queryset = SearchQuerySet().autocomplete(content=query)
        else:
            queryset = EmptySearchQuerySet()
        context['query'] = query
        context['object_list'] = queryset
        return context

    def get_trail_nodes(self):
        trail = super(SearchView, self).get_trail_nodes()
        return trail + [StaticNode(_("Search"), 'search')]
