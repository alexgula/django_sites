# coding=utf-8
from django.conf.urls import *

from .views import FeedbackShow, FeedbackSuccess

urlpatterns = patterns('',
    (r'^$',
        FeedbackShow.as_view(), {}, 'show'),
    (r'^success/$',
        FeedbackSuccess.as_view(), {}, 'success'),
)
