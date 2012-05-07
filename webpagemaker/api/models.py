from django.db import models
from django.conf import settings
from tower import ugettext_lazy as _lazy

class Page(models.Model):
    """
    Represents a Web page that a user has published.
    """

    html = models.TextField(max_length=settings.MAX_PUBLISHED_PAGE_SIZE,
                            verbose_name=_lazy(u'HTML'))
    original_url = models.URLField(blank=True, default='')
