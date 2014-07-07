# coding=utf-8
from django.utils.translation import ugettext_lazy as _
from navigation.views import NavigationTemplateView, HomeNavigationView
from navigation.models import StaticNode
from haystack.query import SearchQuerySet, EmptySearchQuerySet


class SearchView(NavigationTemplateView):
    template_name = 'search/search.html'
    trail_parent = HomeNavigationView
    trail = StaticNode(_("Search"), 'search')

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        query = self.request.GET.get('q', u"")
        if query:
            queryset = SearchQuerySet().autocomplete(content=query)
        else:
            queryset = EmptySearchQuerySet()
        context['search_query'] = query
        context['object_list'] = queryset
        return context
