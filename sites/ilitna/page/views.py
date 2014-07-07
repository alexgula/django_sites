# coding=utf-8
from navigation.views import HomeNavigationView, NavigationDetailView
from .models import Page


class PageDetailView(NavigationDetailView):
    model = Page
    trail_parent = HomeNavigationView

    def get_trail_nodes(self):
        trail = super(PageDetailView, self).get_trail_nodes()
        return trail + [self.object.get_ancestors(), self.object]
