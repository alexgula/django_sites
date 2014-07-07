# coding=utf-8
from django.core.mail import send_mail
from django.template.context import Context
from django.template import loader
from django.utils.translation import ugettext_lazy as _
from constance import config


def send_feedback_notification(feedback):
    subject = _(u"Feedback message") + u": {}".format(feedback.topic)
    from_email = config.FEEDBACK_SENDER

    context = Context({'obj': feedback})
    message = loader.get_template('feedback/feedback_email.msg').render(context)
    recipient_list = config.FEEDBACK_RECIPIENTS,

    send_mail(subject, message, from_email, recipient_list)
