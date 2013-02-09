from django.conf.urls.defaults import patterns, include

from . import views

urlpatterns = patterns('',
    (r'^api/config$', views.get_sanitizer_config),
    (r'^api/page$', views.publish_page),
    (r'^p/(?P<page_id>[A-Za-z0-9]+)/$', views.get_page),
    (r'^p/(?P<page_id>[A-Za-z0-9]+)/raw$', views.get_page_source),
    (r'^p/(?P<page_id>[A-Za-z0-9]+)/edit$',
     'webpagemaker.editor.views.editor', {'remix': views.get_page}),
)
