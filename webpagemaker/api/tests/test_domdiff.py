from nose.tools import eq_

from ..domdiff import diff

def test_equality_returns_empty_set():
    eq_(diff('<p>h</p>', "<p>h</p>"), [])

def test_elements_are_found():
    eq_(diff('<p>h</p>', "h"), [u'p'])

def test_attributes_are_found():
    eq_(diff('<p foo="1">h</p>', "<p>h</p>"), [u'p[foo]'])

def test_unicode_is_encoded():
    uni = u'<p>h\u2026</p>'
    utf8 = uni.encode('utf8')

    eq_(diff(utf8, uni), [])
    eq_(diff(uni, utf8), [])

    eq_(diff(u'<p>h</p>', "h"), [u'p'])
    eq_(diff('<p>h</p>', u"h"), [u'p'])
