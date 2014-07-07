# coding=utf-8
from django.core.mail import send_mail
from django.conf import settings
from django.template.context import Context
from django.template import loader
from django.utils.translation import ugettext_lazy as _


def send_feedback_notification(feedback):
    subject = _(u"Feedback message")
    from_email = settings.FEEDBACK_SENDER

    context = Context({'obj': feedback})
    message = loader.get_template('feedback/feedback_email.msg').render(context)
    recipient_list = settings.FEEDBACK_RECIPIENTS

    send_mail(subject, message, from_email, recipient_list)
