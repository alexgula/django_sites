# coding=utf-8
from django.utils.translation import ugettext_lazy as _

from navigation.views import HomeNavigationView, NavigationListView, NavigationDetailView
from navigation.models import StaticNode
from .models import News, StaticPage


class NewsListView(NavigationListView):
    model = News
    trail_parent = HomeNavigationView
    trail = StaticNode(_("News"), 'news_list')


class NewsDetailView(NavigationDetailView):
    model = News
    trail_parent = NewsListView


class StaticPageView(NavigationDetailView):
    model = StaticPage
    trail_parent = HomeNavigationView
