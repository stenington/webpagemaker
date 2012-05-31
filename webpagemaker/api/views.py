from urlparse import urlparse

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from cors import development_cors

from . import models
from . import sanitize

@csrf_exempt
@require_POST
@development_cors
def publish_page(request):
    if not request.POST.get('html', ''):
        return HttpResponseBadRequest("HTML body expected.")
    if len(request.POST['html']) > settings.MAX_PUBLISHED_PAGE_SIZE:
        return HttpResponse("Request Entity Too Large", status=413)
    if request.POST.get('original-url', ''):
        parsed = urlparse(request.POST['original-url'])
        if parsed.scheme not in ['http', 'https']:
            return HttpResponseBadRequest("Invalid origin URL.")
    trunc = models.Page._meta.get_field_by_name('original_url')[0].max_length
    original_url = request.POST.get('original-url', '')[:trunc]
    page = models.Page(html=request.POST['html'],
                       original_url=original_url)
    page.save()

    # After saving, we now have an ID, which we can use to generate a
    # unique short URL ID and then re-save.
    page.short_url_id = models.rebase(page.id)
    page.save()

    short_url = reverse(get_page, kwargs={'page_id': page.short_url_id})
    response = HttpResponse(short_url, content_type="text/plain")
    return response


@development_cors
def get_sanitizer_config(request):
    cfg = {
        'allowed_tags': sanitize.ALLOWED_TAGS,
        'allowed_attributes': sanitize.ALLOWED_ATTRS
    }
    response = HttpResponse(json.dumps(cfg), content_type="application/json")
    return response

@development_cors
def get_page(request, page_id):
    page = get_object_or_404(models.Page, short_url_id=page_id)
    response = HttpResponse(sanitize.sanitize(page.html))
    if page.original_url:
        response['X-Original-URL'] = page.original_url
    response['X-Robots-Tag'] = 'noindex, nofollow'
    return response
