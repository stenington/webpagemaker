from django.db import models
from django.conf import settings
from tower import ugettext_lazy as _lazy

NUMERALS = "Zv0w2x4y6z8AaBcCeDgEiFkGmHoIqJsKuL3M7NbOfPjQnRrS1T9UhVpW5XlYdt"

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
