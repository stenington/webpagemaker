from django.http import HttpResponse, HttpResponseBadRequest
import urllib2

def slurp(request):
    """
    Endpoint for mission authors to test things out.
    """
    
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
        finalurl = f.geturl().encode('utf8')
        html = f.read().replace('<base href=".">',
                                '<base href="%s">' % finalurl)
        response = HttpResponse(html)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    return HttpResponseBadRequest('need url')
