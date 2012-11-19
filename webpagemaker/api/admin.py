from django.contrib import admin

from . import models

def view_link(obj):
    href = "/p/%s" % obj.short_url_id
    return '<a href="%s">view page at %s</a>' % (href, href)

view_link.short_description = "View link"
view_link.allow_tags = True

def page_size(obj):
    return str(len(obj.html))
    
page_size.short_description = 'Number of characters'

class PageAdmin(admin.ModelAdmin):
    list_display = ('short_url_id', 'original_url', page_size, view_link)
    search_fields = ['short_url_id']

admin.site.register(models.Page, PageAdmin)
