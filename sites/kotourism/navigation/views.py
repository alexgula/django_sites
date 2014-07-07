# coding=utf-8
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from .models import Trail, StaticNode


class NavigationViewMixin(object):

    def get_trail_nodes(self):
        """Return iterable of trail nodes, starting from the root to the leaf."""
        return ()

    def get_trail(self):
        nodes = self.get_trail_nodes()
        return Trail(*nodes)

    def get_context_data(self, **kwargs):
        context = super(NavigationViewMixin, self).get_context_data(**kwargs)
        context['trail'] = self.get_trail()
        return context


class NavigationListView(NavigationViewMixin, ListView):

    def get_context_data(self, **kwargs):
        context = super(NavigationListView, self).get_context_data(**kwargs)
        context['trail'] = self.get_trail()
        return context


class NavigationDetailView(NavigationViewMixin, DetailView):

    def get_context_data(self, **kwargs):
        context = super(NavigationDetailView, self).get_context_data(**kwargs)
        context['trail'] = self.get_trail()
        return context


class HomeNavigationMixin(NavigationViewMixin):
    """Default trail to the home (front page)."""

    def get_trail_nodes(self):
        return [StaticNode(_("Home"), 'home')]


class TemplateNavigationView(HomeNavigationMixin, TemplateView):
    """Trail to the static view."""
    trail = []

    def __init__(self, **kwargs):
        self.trail = kwargs.pop('trail', [])
        super(TemplateNavigationView, self).__init__(**kwargs)

    def get_trail_nodes(self):
        trail = super(TemplateNavigationView, self).get_trail_nodes()
        return trail + [self.trail]

    def get_context_data(self, **kwargs):
        context = super(TemplateNavigationView, self).get_context_data(**kwargs)
        context['trail'] = self.get_trail()
        return context
