from django.http import HttpResponse, HttpResponseRedirect
import jingo

def home(request):
    return jingo.render(request, "website/home.html")

def projects(request):
    return jingo.render(request, "website/projects.html")

def gallery(request):
    return jingo.render(request, "website/gallery.html")

def about(request):
    return jingo.render(request, "website/about.html")

def editor(request):
    return HttpResponseRedirect('http://toolness.github.com/friendlycode/')
