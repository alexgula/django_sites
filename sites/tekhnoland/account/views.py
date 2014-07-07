# coding=utf-8
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib import messages
from .models import Registration
from .forms import RegistrationForm, CustomerProfileForm
from .email import send_activation_email, send_registration_notification, send_edit_profile_notification_email
from ..navigation.models import StaticNode
from ..news.models import News
from ..navigation.views import NavigationViewMixin, ContextTrailMixin, NavigationTemplateView, NavigationUpdateView, HomeNavigationView
from picassoft.utils.classviews import LoginRequiredMixin

@receiver(user_logged_in)
def show_latest_news(sender, user, request, **kwargs):
    latest_news = News.objects.filter(active=True)[:1]
    for news in latest_news:
        messages.info(request, news.text)


class Register(NavigationViewMixin, ContextTrailMixin, CreateView):
    model = Registration
    form_class = RegistrationForm
    success_url = reverse_lazy('account:register_done')
    template_name = 'registration/register_form.html'
    trail_parent = HomeNavigationView
    trail = StaticNode(u"Регистрация", 'account:register')

    def form_valid(self, form):
        # Call super to initialize self.object
        result = super(Register, self).form_valid(form)
        send_activation_email(self.request, self.object)
        return result


class RegisterDone(TemplateView):
    template_name = 'registration/register_done.html'


class RegisterConfirm(TemplateView):
    template_name = 'registration/register_error.html'

    def get(self, request, *args, **kwargs):
        activation_key = self.kwargs['activation_key']
        try:
            Registration.objects.activate(activation_key)
            send_registration_notification(request, activation_key)
        except Exception, e:
            return super(RegisterConfirm, self).get(request, *args, error=e)
        return redirect('account:register_complete')


class RegisterComplete(TemplateView):
    template_name = 'registration/register_complete.html'


class CustomerProfileEdit(LoginRequiredMixin, NavigationUpdateView):
    template_name = 'account/profile_form.html'
    trail_parent = HomeNavigationView
    trail = StaticNode(u"Профиль пользователя", 'account:profile')
    form_class = CustomerProfileForm
    success_url = reverse_lazy('account:profile_done')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        # Call super to initialize self.object
        result = super(CustomerProfileEdit, self).form_valid(form)
        send_edit_profile_notification_email(self.request, self.object)
        return result


class CustomerProfileEditDone(NavigationTemplateView):
    template_name = 'account/profile_done.html'
    trail_parent = HomeNavigationView
    trail = StaticNode(u"Профиль пользователя изменён", 'account:profile_done')
