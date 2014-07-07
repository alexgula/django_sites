# coding=utf-8
import json
from django import http
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView
from django.views.generic.list import MultipleObjectTemplateResponseMixin, BaseListView


class JSONRequestMixin(object):
    def parse_request(self):
        cart_json = self.request.body
        return json.loads(cart_json)


class JSONResponseMixin(object):
    def render_to_response(self, context, **httpresponse_kwargs):
        """Returns a JSON response containing 'context' as payload"""
        return self.get_json_response(self.convert_context_to_json(context), **httpresponse_kwargs)

    @staticmethod
    def get_json_response(content, **httpresponse_kwargs):
        """Construct an `HttpResponse` object."""
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    @staticmethod
    def convert_context_to_json(context):
        # Remove view reference if exists since view object cannot be dumped (was added in Django 1.5)
        if 'view' in context:
            del context['view']
        return json.dumps(context)

    @property
    def is_json(self):
        """Check if the current view is actually have to return JSON.

        Currently checks for either:
        - request's is_ajax() function
        - 'format=json' GET argument in request."""
        return self.request.is_ajax() or self.request.GET.get('format', 'html') == 'json'


class SingleObjectJSONResponseMixin(JSONResponseMixin, BaseDetailView):
    pass


class JSONDetailView(SingleObjectJSONResponseMixin, BaseDetailView):
    pass


class HybridDetailView(SingleObjectJSONResponseMixin, SingleObjectTemplateResponseMixin, BaseDetailView):
    def render_to_response(self, context):
        if self.is_json:
            return SingleObjectJSONResponseMixin.render_to_response(self, context)
        else:
            return SingleObjectTemplateResponseMixin.render_to_response(self, context)


class MultipleObjectJSONResponseMixin(JSONResponseMixin):
    def render_to_response(self, context):
        """Remove object_list if context_object_name is set to avoid unnecessary serializing."""
        context_object_name = self.get_context_object_name(context['object_list'])
        if context_object_name is not None:
            del context['object_list']
        return super(MultipleObjectJSONResponseMixin, self).render_to_response(context)


class JSONListView(MultipleObjectJSONResponseMixin, BaseListView):
    def get_context_data(self, **kwargs):
        if self.is_json:
            kwargs['object_list'] = [self.prepare_to_dump(obj) for obj in kwargs['object_list']]
        return super(JSONListView, self).get_context_data(**kwargs)


class HybridListView(MultipleObjectJSONResponseMixin, MultipleObjectTemplateResponseMixin, BaseListView):
    def get_context_data(self, **kwargs):
        if self.is_json:
            kwargs['object_list'] = [self.prepare_to_dump(obj) for obj in kwargs['object_list']]
        return super(HybridListView, self).get_context_data(**kwargs)

    def render_to_response(self, context):
        if self.is_json:
            return MultipleObjectJSONResponseMixin.render_to_response(self, context)
        else:
            return MultipleObjectTemplateResponseMixin.render_to_response(self, context)


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
