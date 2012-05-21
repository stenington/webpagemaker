import cStringIO as StringIO

import html5lib
from html5lib import treebuilders

def _child_elements(node):
    return [child for child in node.childNodes
            if child.nodeType == child.ELEMENT_NODE]

def _selectors(html):
    htmlfile = StringIO.StringIO(html)
    parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("dom"))
    doc = parser.parse(htmlfile, encoding='utf8')
    nodes = _child_elements(doc)
    result = set()
    while nodes:
        node = nodes.pop()
        result.add(node.nodeName)
        for attr in node.attributes.keys():
            result.add("%s[%s]" % (node.nodeName, attr))
        nodes.extend(_child_elements(node))
    return result

def diff(superset, subset):
    """
    Returns a list of CSS selectors that have at least one match in the
    superset HTML but don't match anything in the subset HTML. Useful
    for detecting what elements and attributes have been stripped out
    during sanitization.
    """
    
    if isinstance(superset, unicode):
        superset = superset.encode('utf8')
    if isinstance(subset, unicode):
        subset = subset.encode('utf8')
    l = list(_selectors(superset).difference(_selectors(subset)))
    l.sort()
    return l
