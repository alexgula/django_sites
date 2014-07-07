# coding=utf-8
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from constance import config
from .forms import FeedbackForm
from .models import Feedback
from .email import send_feedback_notification
from navigation.views import NavigationCreateView, NavigationTemplateView
from navigation.models import StaticNode
from common.views import HomeNavigationView
from content.models import StaticPage


class FeedbackShow(NavigationCreateView):
    model = Feedback
    form_class = FeedbackForm
    success_url = reverse_lazy('feedback:success')
    trail_parent = HomeNavigationView

    def get_trail_nodes(self):
        trail = super(FeedbackShow, self).get_trail_nodes()
        self.page_object = None
        try:
            self.page_object = StaticPage.objects.get(slug=config.FEEDBACK_PAGE_SLUG)
            trail.append(self.page_object)
        except StaticPage.DoesNotExist:
            trail.append(StaticNode(_("Feedback"), 'feedback:show'))
        return trail

    def get_context_data(self, **kwargs):
        context = super(FeedbackShow, self).get_context_data(**kwargs)
        context['object'] = self.page_object
        return context

    def get_form_kwargs(self):
        """Prefill user name and email if user is logged in."""

        kwargs = super(FeedbackShow, self).get_form_kwargs()

        if self.request.user.is_authenticated():
            user = self.request.user
            initial = dict(name=unicode(user), email=user.email)
            kwargs.update(initial=initial)

        return kwargs

    def form_valid(self, form):
        # Call super to initialize self.object
        result = super(FeedbackShow, self).form_valid(form)
        send_feedback_notification(self.object)
        return result


class FeedbackSuccess(NavigationTemplateView):
    template_name = 'feedback/feedback_success.html'
    trail_parent = HomeNavigationView

    def get_trail_nodes(self):
        trail = super(FeedbackSuccess, self).get_trail_nodes()
        self.page_object = None
        try:
            self.page_object = StaticPage.objects.get(slug=config.FEEDBACK_PAGE_SLUG)
            trail.append(self.page_object)
        except StaticPage.DoesNotExist:
            trail.append(StaticNode(_("Feedback"), 'feedback:show'))
        trail.append(StaticNode(_(u"Feedback"), 'feedback:success'))
        return trail
