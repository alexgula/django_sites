# coding=utf-8
from inspect import isclass
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _

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


class ContextTrailMixin(NavigationViewMixin):

    def get_context_data(self, **kwargs):
        context = super(ContextTrailMixin, self).get_context_data(**kwargs)
        nodes = self.get_trail_nodes()
        context['trail'] = Trail(*nodes)
        return context


class NavigationView(ContextTrailMixin, View):
    pass


class NavigationListView(ContextTrailMixin, ListView):
    pass


class NavigationDetailView(ContextTrailMixin, DetailView):
    def get_trail_nodes(self):
        trail = super(NavigationDetailView, self).get_trail_nodes()
        return trail + [self.object]


class NavigationTreeDetailView(ContextTrailMixin, DetailView):
    def get_trail_nodes(self):
        trail = super(NavigationTreeDetailView, self).get_trail_nodes()
        return trail + [self.object.get_ancestors(include_self=True)]


class NavigationTemplateView(ContextTrailMixin, TemplateView):
    pass


class NavigationFormView(ContextTrailMixin, FormView):
    pass


class NavigationCreateView(ContextTrailMixin, CreateView):
    pass


class NavigationUpdateView(ContextTrailMixin, UpdateView):
    pass


class HomeNavigationView(NavigationTemplateView):
    """Default trail to the home (front page)."""
    trail = StaticNode(_("Home"), 'home')
    template_name = 'home.html'
