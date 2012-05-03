from django.conf import settings
from django.conf.urls.defaults import patterns, include

from .api import urls

from funfactory.monkeypatches import patch
patch()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'webpagemaker.website.views.home'),
    (r'^projects', 'webpagemaker.website.views.projects'),
    (r'^gallery', 'webpagemaker.website.views.gallery'),
    (r'^about', 'webpagemaker.website.views.about'),
    (r'^editor', 'webpagemaker.website.views.editor'),
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
        subprocess.check_call(['git', 'submodule', 'update'], cwd=git_root)
        return HttpResponse('git pull succeeded')

    urlpatterns += patterns('',
        (r'^git-pull$', git_pull)
    )

    # And add an endpoint for mission authors to test things out.
    
    def mission_slurp(request):
        from django.http import HttpResponse, HttpResponseBadRequest
        import urllib2
        url = request.GET.get('url')
        if url:
            try:
                f = urllib2.urlopen(url, None, 5)
            except ValueError:
                return HttpResponseBadRequest('bad url')
            except Exception:
                return HttpResponseBadRequest('something terrible happened')
            if f.info().gettype() != 'text/html':
                return HttpResponseBadRequest('can only get html')
            html = f.read().replace('<base href=".">',
                                    '<base href="%s">' % f.geturl())
            response = HttpResponse(html)
            response['Access-Control-Allow-Origin'] = '*'
            return response
        return HttpResponseBadRequest('need url')
    
    urlpatterns += patterns('',
        (r'^mission-slurp$', mission_slurp)
    )
    