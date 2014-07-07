# coding=utf-8
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from common.views import HomeNavigationView
from navigation.models import StaticNode
from navigation.views import NavigationListView, NavigationDetailView
from .models import News, StaticPage


class NewsListView(NavigationListView):
    model = News
    trail_parent = HomeNavigationView
    trail = StaticNode(_("News"), 'news_list')

    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        context['object'] = StaticPage.objects.get(slug=News.home_slug)
        return context


class NewsDetailView(NavigationDetailView):
    model = News
    trail_parent = NewsListView


class StaticPageView(NavigationDetailView):
    model = StaticPage
    trail_parent = HomeNavigationView

    def get(self, request, *args, **kwargs):
        if self.kwargs['slug'] == StaticPage.home_slug:
            return redirect('home', permanent=True)
        return super(StaticPageView, self).get(request, *args, **kwargs)
