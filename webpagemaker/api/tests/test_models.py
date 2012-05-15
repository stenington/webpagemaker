from nose.tools import eq_, ok_

from .. import models

def test_rebase_works_when_num_less_than_numerals_length():
    eq_(models.rebase(1, "abcd"), 'b')

def test_rebase_works_when_num_same_as_numerals_length():
    eq_(models.rebase(4, "abcd"), 'ba')

def test_rebase_works_when_num_more_than_numerals_length():
    eq_(models.rebase(5, "abcd"), 'bb')

def test_short_url_id_not_case_insensitive():
    # MySQL is weird and matches case insensitively, so we need to
    # ensure that we don't generate short url ids that are
    # case-insensitively equal.
    for i in range(len(models.NUMERALS)):
        others = models.NUMERALS[:i] + models.NUMERALS[i+1:]
        ok_(models.NUMERALS[i].lower() not in others.lower())
