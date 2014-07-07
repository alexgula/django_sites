# coding=utf-8
from .models import News
from ..navigation.models import StaticNode
from ..navigation.views import HomeNavigationView, NavigationListView


class NewsList(NavigationListView):
    context_object_name = 'news'
    template_name = 'news/news_full_list.html'
    trail_parent = HomeNavigationView
    trail = StaticNode(u'Новости', 'news:list')

    def get_queryset(self):
        news = News.objects.filter(active=True)
        return news
