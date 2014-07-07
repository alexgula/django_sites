# coding=utf-8
from django.utils.translation import ugettext_lazy as _
from navigation.views import HomeNavigationView, NavigationDetailView, NavigationListView
from navigation.models import StaticNode
from .models import News


class NewsListView(NavigationListView):
    model = News
    trail_parent = HomeNavigationView
    trail = StaticNode(_("Newses"), 'news:list')

    def get_queryset(self):
        return super(NewsListView, self).get_queryset().filter(active=True)


class NewsDetailView(NavigationDetailView):
    model = News
    trail_parent = NewsListView

    def get_trail_nodes(self):
        trail = super(NewsDetailView, self).get_trail_nodes()
        return trail + [self.object]
