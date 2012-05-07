from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest

from . import models
from . import sanitize

@csrf_exempt
@require_POST
def publish_page(request):
    if not request.POST.get('html', ''):
        return HttpResponseBadRequest("HTML body expected.")
    if len(request.POST['html']) > settings.MAX_PUBLISHED_PAGE_SIZE:
        return HttpResponse("Request Entity Too Large", status=413)
    page = models.Page(html=request.POST['html'])
    page.save()
    response = HttpResponse('/p/%d' % page.id, content_type="text/plain")
    response['Access-Control-Allow-Origin'] = '*'
    return response

def get_page(request, page_id):
    page = get_object_or_404(models.Page, pk=page_id)
    response = HttpResponse(sanitize.sanitize(page.html))
    response['Access-Control-Allow-Origin'] = '*'
    return response
