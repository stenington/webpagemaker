from django.db import models

from tower import ugettext_lazy as _lazy

class Page(models.Model):
    """
    Represents a Web page that a user has published.
    """

    html = models.TextField(max_length=10000, verbose_name=_lazy(u'HTML'))
