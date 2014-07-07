from django.conf.urls import patterns
from .views import Vote

urlpatterns = patterns('',
    (r'^(?P<poll_id>\d+)/vote/$', Vote.as_view(), {}, 'vote'),
)
