# coding=utf-8
from django.views.generic.base import TemplateResponseMixin


class FeinCMSObjectTemplateResponseMixin(TemplateResponseMixin):
    def get_template_names(self):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if get_template is overridden.
        """
        return [self.object.template.path.format(model=self.object.__class__.__name__.lower())]
