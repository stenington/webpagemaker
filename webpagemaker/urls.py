from django.conf import settings
from django.conf.urls.defaults import patterns, include

from .api import urls

from funfactory.monkeypatches import patch
patch()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'webpagemaker.website.views.home'),
    (r'^projects$', 'webpagemaker.website.views.projects'),
    (r'^gallery$', 'webpagemaker.website.views.gallery'),
    (r'^about$', 'webpagemaker.website.views.about'),
    (r'^editor$', 'webpagemaker.editor.views.default_editor'),
    (r'^editor/blank$', 'webpagemaker.editor.views.blank_page'),
    (r'^projects/(?P<name>[A-Za-z0-9\-_]+)$',
      'webpagemaker.learning_projects.views.render', {}, 'view_project'),
    (r'^projects/(?P<name>[A-Za-z0-9\-_]+)/edit$',
     'webpagemaker.editor.views.editor', {'remix': 'view_project'}),
    (r'', include(urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

## In DEBUG mode, serve media files through Django.
if settings.DEBUG:
    # Remove leading and trailing slashes so the regex matches.
    media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

    # Remove leading and trailing slashes so the regex matches.
    learning_static_url = settings.LEARNING_PROJECTS_STATIC_URL
    learning_static_url = learning_static_url.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % learning_static_url,
         'django.views.static.serve',
         {'document_root': settings.LEARNING_PROJECTS_STATIC_ROOT}),
    )
    
    from . import debugging
    
    urlpatterns += debugging.urlpatterns

if settings.DEV:
    from .learning_projects import dropbox
    
    urlpatterns += dropbox.urlpatterns
