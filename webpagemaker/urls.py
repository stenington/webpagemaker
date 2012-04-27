from django.conf import settings
from django.conf.urls.defaults import patterns, include

from .api import urls

from funfactory.monkeypatches import patch
patch()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'', include(urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

## In DEBUG mode, serve media files through Django.
if settings.DEBUG:
    # Remove leading and trailing slashes so the regex matches.
    media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

    # Also add an endpoint for a github post-commit hook.                       
    from django.views.decorators.csrf import csrf_exempt
    
    @csrf_exempt
    def git_pull(request):
        from django.http import HttpResponse
        import subprocess
        import os
        git_root = os.path.join(os.path.dirname(__file__), '..')
        subprocess.check_call(['git', 'pull'], cwd=git_root)
        return HttpResponse('git pull succeeded')

    urlpatterns += patterns('',
        (r'^git-pull$', git_pull)
    )
