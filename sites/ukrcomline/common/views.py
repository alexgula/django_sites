from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _
from navigation.models import StaticNode
from navigation.views import ContextTrailMixin


class HomeNavigationView(ContextTrailMixin, TemplateView):
    """Default trail to the home (front page)."""
    trail = StaticNode(_("Home"), 'home')
    template_name = "home.html"
