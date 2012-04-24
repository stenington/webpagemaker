from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest

from . import models

def home(request):
    return HttpResponse("Hello, world!", content_type="text/plain")

@csrf_exempt
@require_POST
def publish_page(request):
    body = request.raw_post_data
    if len(body) == 0:
        return HttpResponseBadRequest("HTML body expected.")
    if len(body) > 10000:
        return HttpResponse("Request Entity Too Large", status=413)
    page = models.Page(html=body)
    page.save()
    response = HttpResponse(str(page.id), content_type="text/plain")
    response['Access-Control-Allow-Origin'] = '*'
    return response

def get_page(request, page_id):
    page = get_object_or_404(models.Page, pk=page_id)
    response = HttpResponse(page.html)
    response['Access-Control-Allow-Origin'] = '*'
    return response
