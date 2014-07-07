# coding=utf-8
from django.views.generic.base import TemplateResponseMixin
from tekhnoland.navigation.models import StaticNode
from tekhnoland.navigation.views import NavigationTemplateView, HomeNavigationView


class FeinCMSObjectTemplateResponseMixin(TemplateResponseMixin):

    def get_template_names(self):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if get_template is overridden.
        """
        return [self.object.template.path.format(model=self.object.__class__.__name__.lower())]


class StaticContentView(NavigationTemplateView):
    code = None
    title = None

    def get_template_names(self):
        return ['content/{}.html'.format(self.code)]

    def get_context_data(self, **kwargs):
        context = super(StaticContentView, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def get_trail_nodes(self):
        return HomeNavigationView.get_class_trail_nodes() + [StaticNode(self.title, self.code)]


class HomeStaticContentView(StaticContentView):

    def get_trail_nodes(self):
        return []
