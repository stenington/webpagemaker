"""
    This test suite makes tests out of all the subdirectories of the
    'html' directory.
    
    Suppose there is directory called 'foo' in 'html'. This suite will
    generate a test called test_foo_sanitization which loads
    'foo/in.html', sanitizes it, and compares the result to 'foo/out.html'.
"""

import os

from nose.tools import eq_
from nose.plugins.skip import SkipTest

from webpagemaker.api import sanitize

ROOT = os.path.dirname(__file__)
HTML_DIR = os.path.join(ROOT, 'html')

def init():
    def make_test(dirname):
        def test():
            input_path = os.path.join(HTML_DIR, dirname, 'in.html')
            output_path = os.path.join(HTML_DIR, dirname, 'out.html')
            input_html = open(input_path, 'r').read()
            if input_html.startswith('<!-- SKIP THIS TEST'):
                raise SkipTest()
            output_html = open(output_path, 'r').read()
            eq_(sanitize.sanitize(input_html), output_html)
        
        test.__name__ = 'test_%s_sanitization' % dirname
        globals()[test.__name__] = test
        
    for dirname in os.listdir(HTML_DIR):
        if os.path.isdir(os.path.join(HTML_DIR, dirname)):
            make_test(dirname)

init()
