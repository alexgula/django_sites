# coding=utf-8
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
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
    trail = StaticNode(_(u"Feedback"), 'feedback:show')

    def get_context_data(self, **kwargs):
        context = super(FeedbackShow, self).get_context_data(**kwargs)
        try:
            context['object'] = StaticPage.objects.get(slug='contacts')
        except StaticPage.DoesNotExist:
            pass
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
    trail = StaticNode(_(u"Feedback"), 'feedback:success')
