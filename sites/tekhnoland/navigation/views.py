# coding=utf-8
from inspect import isclass
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView

from .models import Trail, StaticNode


class NavigationViewMixin(object):

    @classmethod
    def get_class_trail_nodes(cls):
        trail = []
        if hasattr(cls, 'trail_parent') and isclass(cls.trail_parent):
            trail = cls.trail_parent.get_class_trail_nodes()
        if hasattr(cls, 'trail') and cls.trail is not None:
            trail.append(cls.trail)
        return trail

    def get_trail_nodes(self):
        """Return iterable of trail nodes, starting from the root to the leaf."""
        return self.get_class_trail_nodes()

    def get_trail(self):
        nodes = self.get_trail_nodes()
        return Trail(*nodes)


class ContextTrailMixin(object):

    def get_context_data(self, **kwargs):
        context = super(ContextTrailMixin, self).get_context_data(**kwargs)
        context['trail'] = self.get_trail()
        return context


class NavigationView(NavigationViewMixin, ContextTrailMixin, View):
    pass


class NavigationListView(NavigationViewMixin, ContextTrailMixin, ListView):
    pass


class NavigationDetailView(NavigationViewMixin, ContextTrailMixin, DetailView):
    pass


class NavigationTemplateView(NavigationViewMixin, ContextTrailMixin, TemplateView):
    pass


class NavigationFormView(NavigationViewMixin, ContextTrailMixin, FormView):
    pass


class NavigationCreateView(NavigationViewMixin, ContextTrailMixin, CreateView):
    pass


class NavigationUpdateView(NavigationViewMixin, ContextTrailMixin, UpdateView):
    pass


class HomeNavigationView(NavigationViewMixin, ContextTrailMixin):
    """Default trail to the home (front page)."""
    trail = StaticNode(u"На главную", 'home')
