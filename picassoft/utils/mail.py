# coding=utf-8
from django.core.mail import get_connection
from django.core.mail.message import EmailMessage


def send_html_mail(subject, message, from_email, recipient_list,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None):
    connection = connection or get_connection(username=auth_user,
                                    password=auth_password,
                                    fail_silently=fail_silently)
    msg = EmailMessage(subject, message, from_email, recipient_list, connection=connection)
    msg.content_subtype = 'html'
    return msg.send()
