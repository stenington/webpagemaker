from nose.tools import ok_
from .. import cosmetics

def same(a, b):
    ok_(cosmetics.are_differences_cosmetic(a, b))

def not_same(a, b):
    ok_(not cosmetics.are_differences_cosmetic(a, b))
    
def test_whitespace_in_open_tag():
    same("<p></p>", "<p \n></p>")

def test_whitespace_in_close_tag():
    same("<p></p>", "<p></p >")

def test_omitted_script_tag():
    not_same("<p>hi <script>u</script></p>", "<p>hi u</p>")
    not_same("<p>hi <script>u</script></p>", "<p>hi </p>")

def test_omitted_attribute():
    not_same('<p onclick="LOL">hi</p>', '<p>hi</p>')

def test_boolean_attribute():
    same('<p blah>hi</p>', '<p blah="">hi</p>')

INDENTED_HTML = """<!DOCTYPE html>
<html>
  <head>
    <title>hi</title>
  </head>
  <body>
    <p>hello!</p>
  </body>
</html>
"""

UNINDENTED_HTML = u'<!DOCTYPE html><html><head>\n    <title>hi</title>\n' \
                  u'  </head>\n  <body>\n    <p>hello!</p>\n  \n\n' \
                  u'</body></html>'

def test_whitespace_in_document():
    same(INDENTED_HTML, UNINDENTED_HTML)
