from nose.tools import eq_

from .. import models

def test_rebase_works_when_num_less_than_numerals_length():
    eq_(models.rebase(1, "abcd"), 'b')

def test_rebase_works_when_num_same_as_numerals_length():
    eq_(models.rebase(4, "abcd"), 'ba')

def test_rebase_works_when_num_more_than_numerals_length():
    eq_(models.rebase(5, "abcd"), 'bb')
