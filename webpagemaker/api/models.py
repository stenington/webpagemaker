from django.db import models
from django.conf import settings
from tower import ugettext_lazy as _lazy

NUMERALS = "3fldc4mzjyqr7bkug5vh0a68xpon9stew12i"

def rebase(num, numerals=NUMERALS):
    base = len(numerals)
    left_digits = num // base
    if left_digits == 0:
        return numerals[num % base]
    else:
        return rebase(left_digits, numerals) + numerals[num % base]

class Page(models.Model):
    """
    Represents a Web page that a user has published.
    """

    html = models.TextField(max_length=settings.MAX_PUBLISHED_PAGE_SIZE,
                            verbose_name=_lazy(u'HTML'))
    original_url = models.URLField(blank=True, default='')
    short_url_id = models.CharField(max_length=10, blank=True)
    creator = models.ForeignKey('auth.User', blank=True, null=True,
                                related_name='pages')
