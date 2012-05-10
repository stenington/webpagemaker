from django.conf.urls.defaults import patterns, include

from . import views

urlpatterns = patterns('',
    (r'^api/config', views.get_sanitizer_config),
    (r'^api/page', views.publish_page),
    (r'p/(?P<page_id>[0-9]+)', views.get_page)
)
