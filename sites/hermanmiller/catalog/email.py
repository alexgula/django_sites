# coding=utf-8
from django.contrib.sites.models import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from picassoft.utils.mail import send_html_mail


def send_review_notification(request, review):
    current_site = get_current_site(request)

    subject = _("Herman Miller product review #{}").format(review.id)
    recipient_list = settings.ORDER_RECIPIENTS
    from_email = settings.ORDER_SENDER

    context = {'object': review, 'site': current_site}
    body = render_to_string('catalog/product_review_notification_email.html', context)

    send_html_mail(subject, body, from_email, recipient_list)

    if review.email:
        send_html_mail(subject, body, from_email, [review.email])
