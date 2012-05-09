from . import git, learning_project_slurp

from django.conf.urls.defaults import patterns, include

urlpatterns = patterns('',
    (r'^git-pull$', git.pull),
    (r'^mission-slurp$', learning_project_slurp.slurp),
    (r'^mission-slurp/proxy/(?P<scheme>(http|https))/' +
     r'(?P<domain>[A-Za-z0-9\-_\.]+)/(?P<path>.*)',
     learning_project_slurp.proxy),
)
