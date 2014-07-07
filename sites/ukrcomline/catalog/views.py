# coding=utf-8
from django.db.models import F
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from common.views import HomeNavigationView
from navigation.models import StaticNode
from navigation.views import NavigationListView, ContextTrailMixin
from .models import Category


class CategoryListView(NavigationListView):
    model = Category
    trail_parent = HomeNavigationView
    trail = StaticNode(_("Categories"), 'category_list')

    def get_queryset(self):
        return Category.objects.root_nodes()

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['title'] = _("Production")
        context['children'] = self.object_list
        return context


class CategoryDetailView(ContextTrailMixin, DetailView):
    model = Category
    trail_parent = CategoryListView

    def get_object(self, queryset=None):
        obj = super(CategoryDetailView, self).get_object(queryset)
        self.show_as_list = not obj.is_leaf_node()
        return obj

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        if self.show_as_list:
            context['children'] = self.object.get_children()
            context['more_children'] = self.object.more_children.filter(rght=F('lft') + 1)
        context['title'] = self.object.title
        return context

    def get_template_names(self):
        self.template_name_suffix = '_list' if self.show_as_list else '_detail'
        return super(CategoryDetailView, self).get_template_names()

    def get_trail_nodes(self):
        trail = super(CategoryDetailView, self).get_trail_nodes()

        cat_id = self.request.GET.get('cat', None)
        cat = None
        if cat_id is not None:
            try:
                cat = Category.objects.get(id=cat_id)
            except Category.DoesNotExist:
                cat = None

        if cat is None:
            return trail + [self.object.get_ancestors(include_self=True)]
        else:
            return trail + [cat] + [cat.get_ancestors(include_self=True)]
