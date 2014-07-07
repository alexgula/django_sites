# coding=utf-8
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.template.base import Template
from django.template.context import Context
from .forms import FeedbackForm
from .models import Feedback
from .email import send_feedback_notification
from ..navigation.views import NavigationCreateView, NavigationTemplateView, HomeNavigationView
from ..navigation.models import StaticNode


FEEDBACK_MESSAGE_TEMPLATE = u"""Новое сообщение из формы обратной связи!

Категория вопроса: {{ obj.get_category_display }}

Имя пользователя: {{ obj.name }}
Email пользователя: {{ obj.email }}
Статус пользователя: {{ obj.get_status_display }}

----------------------------------------
{{ obj.text }}
----------------------------------------
"""

class FeedbackShow(NavigationCreateView):
    model = Feedback
    form_class = FeedbackForm
    success_url = reverse_lazy('feedback:success')
    trail_parent = HomeNavigationView
    trail = StaticNode(u'Обратная связь', 'feedback:show')

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
    trail = StaticNode(u'Обратная связь', 'feedback:success')
