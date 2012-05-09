from django.http import HttpResponse, HttpResponseBadRequest
import urllib2
import urlparse

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
        baseurl = urlparse.urljoin(finalurl, '.')
        info = urlparse.urlparse(baseurl)
        proxybaseurl = "/mission-slurp/proxy/%s/%s%s" % (
            info.scheme,
            info.netloc,
            info.path
            )
        proxybaseurl = request.build_absolute_uri(proxybaseurl)
        html = f.read().replace('<base href=".">',
                                '<base href="%s">' % proxybaseurl)
        response = HttpResponse(html)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    return HttpResponseBadRequest('need url')

def proxy(request, scheme, domain, path):
    url = "%s://%s/%s" % (scheme, domain, path)
    try:
        f = urllib2.urlopen(url, None, 5)
    except ValueError:
        return HttpResponseBadRequest('bad url')
    except urllib2.HTTPError, e:
        return HttpResponse(content="alas, %d." % e.code, status=e.code)
    except Exception:
        return HttpResponseBadRequest('something terrible happened')
    response = HttpResponse(
        f, # Hopefully we are iterating over this.
        content_type=f.info()['content-type']
        )
    response['Access-Control-Allow-Origin'] = '*'
    return response
