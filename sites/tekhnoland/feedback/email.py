# coding=utf-8
from django.core.mail import send_mail
from django.conf import settings
from django.template.base import Template
from django.template.context import Context


FEEDBACK_MESSAGE_TEMPLATE = u"""Новое сообщение из формы обратной связи!

Категория вопроса: {{ obj.get_category_display }}

Имя пользователя: {{ obj.name }}
Email пользователя: {{ obj.email }}
Статус пользователя: {{ obj.get_status_display }}

------------------------------ Текст сообщения --------------------------------

{{ obj.text }}
"""

def send_feedback_notification(feedback):
    subject = u"Сообщение из формы обратной связи сайта Tekhnoland"
    from_email = settings.FEEDBACK_SENDER

    context = Context({'obj': feedback})
    message = Template(FEEDBACK_MESSAGE_TEMPLATE).render(context)
    recipient_list = settings.FEEDBACK_RECIPIENTS

    send_mail(subject, message, from_email, recipient_list)
