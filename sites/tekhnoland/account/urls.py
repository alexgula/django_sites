# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout,\
    password_reset, password_reset_done, password_reset_confirm, password_reset_complete, password_change, password_change_done
from django.core.urlresolvers import reverse_lazy
from .views import Register, RegisterDone, RegisterConfirm, RegisterComplete, CustomerProfileEdit, CustomerProfileEditDone
from .forms import PasswordResetFormHtml

urlpatterns = patterns('',
        url(r'^login/$',
            login, {}, name='login'),
        url(r'^reset/$',
            password_reset, {
                'post_reset_redirect': reverse_lazy('account:reset_done'),
                'password_reset_form': PasswordResetFormHtml
            }, name='reset'),
        url(r'^reset/done/$',
            password_reset_done, {}, name='reset_done'),
        url(r'^reset/confirm/(?P<uidb36>[0-9A-Za-z]+)/(?P<token>.+)/$',
            password_reset_confirm, {'post_reset_redirect': reverse_lazy('account:reset_complete')}, name='reset_confirm'),
        url(r'^reset/complete/$',
            password_reset_complete, {}, name='reset_complete'),
        url(r'^password/$',
            password_change, {
                'post_change_redirect': reverse_lazy('account:password_done'),
            }, name='password'),
        url(r'^password/done/$',
            password_change_done, {}, name='password_done'),

        url(r'^register/$',
            Register.as_view(), {}, name='register'),
        url(r'^register/done/$',
            RegisterDone.as_view(), {}, name='register_done'),
        url(r'^register/confirm/(?P<activation_key>.+)/$',
            RegisterConfirm.as_view(), {}, name='register_confirm'),
        url(r'^register/complete/$',
            RegisterComplete.as_view(), {}, name='register_complete'),

        url(r'^profile/$',
            CustomerProfileEdit.as_view(), {}, name='profile'),
        url(r'^profile/done/$',
            CustomerProfileEditDone.as_view(), {}, name='profile_done'),

        url(r'^logout/$',
            logout, {}, name='logout'),
)
