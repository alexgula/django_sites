# coding=utf-8
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from picassoft.utils.mail import send_html_mail


def send_activation_email(request, author):
    current_site = get_current_site(request)

    subject = _("Registration on site {}").format(current_site.domain)
    recipient_list = [author.email]
    from_email = settings.AUTHOR_REGISTER_SENDER

    context = {'obj': author, 'site': current_site}
    body = render_to_string('photocontest/register_email.html', context)

    return send_html_mail(subject, body, from_email, recipient_list)
