# coding=utf-8
from django.utils.translation import ugettext_lazy as _
from common.views import HomeNavigationView
from navigation.models import StaticNode
from navigation.views import NavigationListView, NavigationDetailView
from .models import News, Portfolio, Certificate, StaticPage


class NewsListView(NavigationListView):
    model = News
    trail_parent = HomeNavigationView
    trail = StaticNode(_("News list"), 'news_list')


class NewsDetailView(NavigationDetailView):
    model = News
    trail_parent = NewsListView


class PortfolioListView(NavigationListView):
    model = Portfolio
    trail_parent = HomeNavigationView
    trail = StaticNode(_("Portfolios"), 'portfolio_list')


class PortfolioDetailView(NavigationDetailView):
    model = Portfolio
    trail_parent = PortfolioListView


class CertificateListView(NavigationListView):
    model = Certificate
    trail_parent = HomeNavigationView
    trail = StaticNode(_("Certificates"), 'certificate_list')


class StaticPageView(NavigationDetailView):
    model = StaticPage
    trail_parent = HomeNavigationView
