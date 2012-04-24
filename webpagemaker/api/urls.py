from django.conf.urls.defaults import patterns, include

from . import views

urlpatterns = patterns('',
    (r'^$', views.home),
    (r'^page', views.publish_page),
    (r'(?P<page_id>[0-9]+)', views.get_page)
)
