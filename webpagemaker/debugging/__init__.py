from . import git

from django.conf.urls.defaults import patterns, include

urlpatterns = patterns('',
    (r'^git-pull$', git.pull),
)
