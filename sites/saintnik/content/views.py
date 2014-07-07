# coding=utf-8
from django.views.generic.base import TemplateResponseMixin
from django.utils.translation import ugettext_lazy as _
from ..navigation.views import HomeNavigationView, NavigationDetailView, NavigationListView
from ..navigation.models import StaticNode
from .models import News, InfoPage, GalleryPage


class FeinCMSObjectTemplateResponseMixin(TemplateResponseMixin):
    def get_template_names(self):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if get_template is overridden.
        """
        return [self.object.template.path.format(model=self.object.__class__.__name__.lower())]


class NewsListView(NavigationListView):
    model = News
    trail_parent = HomeNavigationView
    trail = StaticNode(_("News"), 'news_list')

    def get_queryset(self):
        return super(NewsListView, self).get_queryset().filter(active=True)


class NewsDetailView(NavigationDetailView):
    model = News
    trail_parent = NewsListView

    def get_trail_nodes(self):
        trail = super(NewsDetailView, self).get_trail_nodes()
        return trail + [self.object]


class InfoDetailView(NavigationDetailView):
    model = InfoPage
    trail_parent = HomeNavigationView

    def get_trail_nodes(self):
        trail = super(InfoDetailView, self).get_trail_nodes()
        return trail + [self.object.get_ancestors(), self.object]


class GalleryListView(NavigationListView):
    model = GalleryPage
    trail_parent = HomeNavigationView
    trail = StaticNode(_("Gallery"), 'gallery_list')

    def get_queryset(self):
        return GalleryPage.objects.root_nodes().filter(active=True)


class GalleryDetailView(NavigationDetailView):
    model = GalleryPage
    trail_parent = GalleryListView

    def get_trail_nodes(self):
        trail = super(GalleryDetailView, self).get_trail_nodes()
        return trail + [self.object]
