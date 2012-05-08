from django.contrib import admin

from . import models

def view_link(obj):
    href = "/p/%d" % obj.id
    return '<a href="%s">view page at %s</a>' % (href, href)

view_link.short_description = "View link"
view_link.allow_tags = True

def page_size(obj):
    return str(len(obj.html))
    
page_size.short_description = 'Number of characters'

class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_url', page_size, view_link)

admin.site.register(models.Page, PageAdmin)
