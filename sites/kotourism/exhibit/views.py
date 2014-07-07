# coding=utf-8
from ..navigation.views import HomeNavigationMixin, NavigationDetailView
from ..navigation.models import ModelNode
from .models import Exhibit


class ExhibitDetail(HomeNavigationMixin, NavigationDetailView):
    model = Exhibit

    def get_trail_nodes(self):
        trail = super(ExhibitDetail, self).get_trail_nodes()
        return trail + [ModelNode(self.object)]
