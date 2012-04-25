from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest

import bleach

from . import models

ALLOWED_TAGS = [
    "!doctype", "html", "body", "a", "abbr", "address", "area", "article",
    "aside", "audio", "b", "base", "bdi", "bdo", "blockquote", "body", "br",
    "button", "canvas", "caption", "cite", "code", "col", "colgroup",
    "command", "datalist", "dd", "del", "details", "dfn", "div", "dl", "dt",
    "em", "embed", "fieldset", "figcaption", "figure", "footer", "form",
    "h1", "head", "header", "hgroup", "hr", "html", "i", "iframe", "img",
    "input", "ins", "keygen", "kbd", "label", "legend", "li", "link", "map",
    "mark", "menu", "meta", "meter", "nav", "noscript", "object",
    "ol", "optgroup", "option", "output", "p", "param", "pre", "progress",
    "q", "rp", "rt", "s", "samp", "section", "select", "small", "source", 
    "span", "strong", "style", "sub", "summary", "sup", "table", "tbody", 
    "td", "textarea", "tfoot", "th", "thead", "time", "title", "tr", "track", 
    "u", "ul", "var", "video", "wbr"
    ]

ALLOWED_ATTRS = {
    # TODO: We should probably add to this. What meta attributes can't
    # be abused for SEO purposes?
    "meta": ["charset"]
}

if bleach.VERSION < (1, 1, 1):
    raise Exception("Please use simon wex's bleach fork for now: " +
                    "https://github.com/simonwex/bleach.git")

def home(request):
    return HttpResponse("Hello, world!", content_type="text/plain")

@csrf_exempt
@require_POST
def publish_page(request):
    body = request.raw_post_data
    if len(body) == 0:
        return HttpResponseBadRequest("HTML body expected.")
    if len(body) > settings.MAX_PUBLISHED_PAGE_SIZE:
        return HttpResponse("Request Entity Too Large", status=413)
    page = models.Page(html=body)
    page.save()
    response = HttpResponse('/p/%d' % page.id, content_type="text/plain")
    response['Access-Control-Allow-Origin'] = '*'
    return response

def get_page(request, page_id):
    page = get_object_or_404(models.Page, pk=page_id)
    html = bleach.clean(page.html, strip=True, strip_comments=False,
                        tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS,
                        parse_as_fragment=False)
    response = HttpResponse(html)
    response['Access-Control-Allow-Origin'] = '*'
    return response
