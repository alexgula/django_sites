from copy import copy
from django.db.models import Q
from django.utils.translation import ugettext as _

from .models import LifePeriod, Term, Category, Author

from picassoft.utils.views import params_format

def build_params(dict):
    def set_param(params, dict, field):
        params[field] = set(dict.getlist(field))
    params = {}
    set_param(params, dict, 'period')
    for category in Category.objects.all():
        set_param(params, dict, category.slug)
    return params

def build_filters(params, author_slug=None):
    # Filter by author periods
    part_filter = Filter(_("Life periods"), params, 'period')
    if author_slug:
        periods = LifePeriod.objects.order_by('year_begin', 'year_end').filter(author__slug=author_slug)
        for period in periods:
            query = Q(periods__slug=period.slug)
            part_filter.add_term(period.name, period.slug, query)

    category_filters = {}
    for term in Term.objects.order_by('category__weight').select_related(depth=1):
        category = term.category
        filter = category_filters.get(category.slug, Filter(category.name, params, category.slug))
        query = Q(terms__slug=term.slug)
        filter.add_term(term.name, term.slug, query)
        category_filters[category.slug] = filter

    return [part_filter] + category_filters.values()

def make_title(filters):
    names = []
    for filter in filters:
        params = filter.params[filter.slug]
        if params:
            terms_text = u', '.join([term.name for term in filter.terms if term.chosen])
            names.append(u'{0}: {1}'.format(filter.name, terms_text))
    return u' | '.join(names)


class Filter(object):
    def __init__(self, name, params, slug):
        self.name = name
        self.params = params
        self.slug = slug
        self.terms = []
        self.chosen_terms = 0
        self.available_terms = 0

    @property
    def has_visible_terms(self):
        for term in self.terms:
            if term.visible:
                return True
        return False

    def calc_facets(self, queryset, filters):
        for filter in filters:
            if filter is not self and filter.chosen_terms > 0:
                query = Q()
                for term in filter.terms:
                    if term.chosen:
                        query = query | term.query
                if query:
                    queryset = queryset.filter(query)

        from django.http import QueryDict
        for node in queryset.all():
            dict = QueryDict(node.filter)
            term_values = dict.getlist(self.slug)
            for term in self.terms:
                if term.slug in term_values:
                    term.occurences += 1

    def add_term(self, *args):
        self.terms.append(FilterTerm(*((self,) + args)))

    def build_query(self):
        query = Q()
        for term in self.terms:
            if term.chosen:
                query = query | term.query
        return query

    def build_clear_params(self):
        """Build parameters to remove all terms in the filter."""
        from django.http import QueryDict
        dict = QueryDict(u"", mutable=True)
        for key, values in self.params.iteritems():
            if key != self.slug:
                dict.setlist(key, values)
        return params_format(dict)


class FilterTerm(object):
    def __init__(self, filter, name, slug, query):
        self.filter = filter
        self.name = name
        self.slug = slug
        self.query = query
        self.occurences = 0

        self.params = copy(self.filter.params)
        values = copy(self.params.get(self.filter.slug, set()))

        if slug in values:
            self.chosen = True
            self.filter.chosen_terms += 1
            values.remove(slug)
        else:
            self.chosen = False
            self.filter.available_terms += 1
            values.add(slug)

        self.params[self.filter.slug] = values

    @property
    def visible(self):
        return self.chosen or self.occurences > 0

    def build_modify_params(self):
        """Build parameters for adding/removing term from selection."""
        from django.http import QueryDict
        dict = QueryDict(u"", mutable=True)
        for key, values in self.params.iteritems():
            dict.setlist(key, values)
        return params_format(dict)

    def build_select_params(self):
        """Build parameters for selecting only this term in filter."""
        from django.http import QueryDict
        dict = QueryDict(u"", mutable=True)
        for key, values in self.params.iteritems():
            if key == self.filter.slug:
                dict.appendlist(key, self.slug)
            else:
                dict.setlist(key, values)
        return params_format(dict)
