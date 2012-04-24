#!/usr/bin/env python

import sys, os

# This is to avoid the ImportError: No module named web on petri

abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)

import web
import redis
import bleach

ALLOWED_TAGS = ["!doctype", "html", "body", "a", "abbr", "address", "area", "article", "aside", "audio", "b", "base", "bdi", "bdo", "blockquote", "body", "br", "button", "canvas", "caption", "cite", "code", "col", "colgroup", "command", "datalist", "dd", "del", "details", "dfn", "div", "dl", "dt", "em", "embed", "fieldset", "figcaption", "figure", "footer", "form", "h1", "head", "header", "hgroup", "hr", "html", "i", "iframe", "img", "input", "ins", "keygen", "kbd", "label", "legend", "li", "link", "map", "mark", "menu", {"meta": "*"}, "meter", "nav", "noscript", "object", "ol", "optgroup", "option", "output", "p", "param", "pre", "progress", "q", "rp", "rt", "s", "samp", "section", "select", "small", "source", "span", "strong", "style", "sub", "summary", "sup", "table", "tbody", "td", "textarea", "tfoot", "th", "thead", "time", "title", "tr", "track", "u", "ul", "var", "video", "wbr"]

urls = (
    '/', 'Index',
    '/page', 'Page',
    '/(.*?)$', 'Page',
)

REDIS_CREDENTIALS = None

if 'VCAP_SERVICES' in os.environ:
    import json
    vcap_services = json.loads(os.environ['VCAP_SERVICES'])
    REDIS_CREDENTIALS = vcap_services["redis-2.2"][0]["credentials"]
else:
    REDIS_CREDENTIALS = {'hostname':'localhost', 'port':6379, 'password':None}
    
def redis_connect():
    return redis.StrictRedis(host=REDIS_CREDENTIALS['hostname'], port=REDIS_CREDENTIALS['port'], password=REDIS_CREDENTIALS['password'])
    
def rebase(num, numerals="Zv0w2x4y6z8AaBcCeDgEiFkGmHoIqJsKuL3M7NbOfPjQnRrS1T9UhVpW5XlYdt"):
    base = len(numerals)
    left_digits = num // base
    if left_digits == 0:
        return numerals[num % base]
    else:
        return baseN(left_digits, base, numerals) + numerals[num % base]

class Page:
    def POST(self):
        web.header('Access-Control-Allow-Origin','*', unique=True) 
        r = redis_connect()
        
        # Get a new id from redis
        page_id = int(r.incr('global:last_page_id'))
        
        # Pull out the raw POST data.
        data = web.data()
        
        # Compute the short url key
        key = rebase(page_id)
        
        r.set('page:%s' % key, data)
        
        return key
        
    def GET(self, id):
        web.header('Access-Control-Allow-Origin','*', unique=True) 
        r = redis_connect()
        data = r.get('page:%s' % id)
        
        print 'page:%s' % id
        
        if data == None:
            raise web.notfound()
        
        return bleach.clean(data, strip=True, strip_comments=False, tags=ALLOWED_TAGS)

class Index:
    def GET(self):
        return "Hello, world!"


# This is used for wsgi (aka Petri)
application = web.application(urls, globals()).wsgifunc()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
