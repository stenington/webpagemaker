import jingo

def home(request):
    return jingo.render(request, "website/home.html")

def projects(request):
    return jingo.render(request, "website/projects.html")

def gallery(request):
    return jingo.render(request, "website/gallery.html")

def about(request):
    return jingo.render(request, "website/about.html")

def webarcade(request):
    return jingo.render(request, "website/webarcade.html")

def guidelines(request):
    return jingo.render(request, "website/content-guidelines.html")
