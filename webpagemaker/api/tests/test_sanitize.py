"""
    This test suite makes tests out of all the Markdown files in the
    'html' directory.
    
    Each Markdown file (other than README.md) should contain
    only one or two HTML snippets. The first snippet is always the
    input to the sanitizer, and the second snippet, if present, is the
    expected output. If no second snippet is present, the expected
    output is the same as the input.
    
    If the Markdown file ever contains the line '## SKIP THIS TEST', then
    the test is skipped via a SkipTest exception.
"""

import os

from nose.tools import eq_
from nose.plugins.skip import SkipTest

from webpagemaker.api import sanitize

ROOT = os.path.dirname(__file__)
HTML_DIR = os.path.join(ROOT, 'html')

def init():
    def make_test(filename):
        skip_test = False
        snippets = []
        in_snippet = False
        input_html = None
        output_html = None
        
        for line in open(os.path.join(HTML_DIR, filename), 'r'):
            if line.upper().startswith("## SKIP THIS TEST"):
                skip_test = True
            if line.strip() == '```html':
                in_snippet = True
                snippets.append([])
            elif line.strip() == '```':
                in_snippet = False
            elif in_snippet:
                snippets[-1].append(line)

        def test():
            if skip_test:
                raise SkipTest()
            if len(snippets) == 1:
                input_html = ''.join(snippets[0]).strip()
                output_html = input_html
            elif len(snippets) == 2:
                input_html = ''.join(snippets[0]).strip()
                output_html = ''.join(snippets[1]).strip()
            else:
                raise Exception("Cannot identify snippets in %s." % filename)

            eq_(sanitize.sanitize(input_html), output_html)

        test.__name__ = 'test_%s' % filename.split('.')[0]
        
        if len(snippets) == 1:
            test.__doc__ = "%s (idempotency test)" % filename
        elif len(snippets) == 2:
            test.__doc__ = "%s (sanitization test)" % filename

        globals()[test.__name__] = test

    for filename in os.listdir(HTML_DIR):
        if filename.endswith('.md') and filename != 'README.md':
            make_test(filename)

init()
