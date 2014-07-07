# coding=utf-8
from django.views.generic.detail import DetailView
from common.views import HomeNavigationView
from navigation.views import ContextTrailMixin
from .models import Category


class CategoryDetailView(ContextTrailMixin, DetailView):
    model = Category
    trail_parent = HomeNavigationView

    def get_object(self, queryset=None):
        obj = super(CategoryDetailView, self).get_object(queryset)
        self.show_as_list = not obj.is_leaf_node()
        return obj

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        if self.show_as_list:
            context['category_list'] = self.object.get_children()
        context['title'] = self.object.title
        return context

    def get_template_names(self):
        self.template_name_suffix = '_list' if self.show_as_list else '_detail'
        return super(CategoryDetailView, self).get_template_names()

    def get_trail_nodes(self):
        trail = super(CategoryDetailView, self).get_trail_nodes()
        return trail + [self.object.get_ancestors(include_self=True)]
