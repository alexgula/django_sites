from django.utils.translation import ugettext_lazy as _
from navigation.models import StaticNode
from navigation.views import NavigationDetailView
from content.models import StaticPage


class HomeNavigationView(NavigationDetailView):
    """Default trail to the home (front page)."""
    trail = StaticNode(_("Home"), 'home')
    model = StaticPage
    template_name = 'home.html'

    def get_object(self, queryset=None):
        self.kwargs['slug'] = StaticPage.home_slug
        return super(HomeNavigationView, self).get_object(queryset)
