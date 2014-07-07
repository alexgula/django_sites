# coding=utf-8
from django.utils.translation import ugettext_lazy as _
from ..navigation.models import StaticNode
from ..navigation.views import HomeNavigationMixin, NavigationListView
from .models import Partner


from sorl.thumbnail import base
base.EXTENSIONS.update({'GIF': 'gif'})


class PartnerList(HomeNavigationMixin, NavigationListView):
    model = Partner

    def get_trail_nodes(self):
        return super(PartnerList, self).get_trail_nodes() + [StaticNode(_("Regions"), 'partner_list')]
