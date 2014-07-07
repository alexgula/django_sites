# coding=utf-8
from django.utils.http import int_to_base36
from django.contrib.sites.models import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from picassoft.utils.mail import send_html_mail
from .models import Registration

def send_password_reset_email(request, user, email_template_name, token_generator):
    current_site = get_current_site(request)

    subject = u"Обновление пароля на сайте Tekhnoland"
    recipient_list = [user.email]
    from_email = settings.REGISTER_SENDER

    context = {
        'user': user,
        'uid': int_to_base36(user.id),
        'token': token_generator.make_token(user),
        'site': current_site,
    }
    body = render_to_string(email_template_name, context)

    return send_html_mail(subject, body, from_email, recipient_list)

def send_activation_email(request, registration):
    current_site = get_current_site(request)

    subject = u"Регистрация на сайте Tekhnoland"
    recipient_list = [registration.email]
    from_email = settings.REGISTER_SENDER

    context = {'obj': registration, 'site': current_site}
    body = render_to_string('registration/register_email.html', context)

    return send_html_mail(subject, body, from_email, recipient_list)

def send_registration_notification(request, registration_key):
    current_site = get_current_site(request)

    registration = Registration.objects.get(activation_key=registration_key)

    subject = u"Регистрация на сайте Tekhnoland"
    recipient_list = settings.REGISTER_RECIPIENTS
    from_email = settings.REGISTER_SENDER

    context = {'obj': registration, 'site': current_site}
    body = render_to_string('registration/register_notification_email.html', context)

    return send_html_mail(subject, body, from_email, recipient_list)

def send_edit_profile_notification_email(request, customer_profile):
    current_site = get_current_site(request)

    subject = u"Обновление профиля пользователя на сайте Tekhnoland"
    recipient_list = settings.REGISTER_RECIPIENTS
    from_email = settings.REGISTER_SENDER

    context = {'obj': customer_profile, 'site': current_site}
    body = render_to_string('registration/edit_profile_notification_email.html', context)

    return send_html_mail(subject, body, from_email, recipient_list)
