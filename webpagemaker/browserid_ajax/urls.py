from django.conf.urls.defaults import patterns

from . import views

urlpatterns = patterns('',
    (r'^status', views.get_status, {}, 'browserid_ajax_get_status'),
    (r'^logout', views.logout, {}, 'browserid_ajax_logout'),
    (r'^verify', views.verify, {}, 'browserid_ajax_verify')
)
