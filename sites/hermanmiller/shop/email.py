# coding=utf-8
from django.contrib.sites.models import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from picassoft.utils.mail import send_html_mail


class EmailMixin(object):
    def send_order_notification(self, order):
        current_site = get_current_site(self.request)

        subject = _("Herman Miller order #{}").format(order.id)
        recipient_list = settings.ORDER_RECIPIENTS
        from_email = settings.ORDER_SENDER

        context = {'object': order, 'site': current_site}
        body = render_to_string('shop/order_notification_email.html', context)

        send_html_mail(subject, body, from_email, recipient_list)

        if order.email:
            send_html_mail(subject, body, from_email, [order.email])
