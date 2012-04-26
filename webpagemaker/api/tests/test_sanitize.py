"""
    This test suite makes tests out of all the HTML files in the
    'html' directory.
    
    Suppose there is a file called 'foo.in.html'. This suite will
    generate a test called test_foo_sanitization which loads
    'foo.in.html', sanitizes it, and compares the result to 'foo.out.html'.
"""

import os
import glob

from nose.tools import eq_
from nose.plugins.skip import SkipTest

from webpagemaker.api import sanitize

ROOT = os.path.dirname(__file__)
HTML_DIR = os.path.join(ROOT, 'html')
TEST_PAGES = glob.glob(os.path.join(HTML_DIR, '*.out.html'))

def init():
    def make_test(published_path):
        published_filename = os.path.basename(published_path)
        testname = published_filename.split('.')[0]
        input_filename = "%s.in.html" % testname
        input_path = os.path.join(HTML_DIR, input_filename)
        
        def test():
            input_html = open(input_path, 'r').read()
            if input_html.startswith('<!-- SKIP THIS TEST'):
                raise SkipTest()
            published_html = open(published_path, 'r').read()
            eq_(sanitize.sanitize(input_html), published_html)
        
        test.__name__ = 'test_%s_sanitization' % testname
        globals()[test.__name__] = test
        
    for published_path in TEST_PAGES:
        make_test(published_path)

init()
