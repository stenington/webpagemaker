import html5lib
from html5lib import treebuilders, treewalkers, serializer

def _normalize(html):
    """
    Normalize the given string of HTML, collapsing whitespace.
    """
    
    # This is taken from the "Serialization of Streams" section of
    # http://code.google.com/p/html5lib/wiki/UserDocumentation.
    p = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("dom"))
    dom_tree = p.parse(html)
    walker = treewalkers.getTreeWalker("dom")
    stream = walker(dom_tree)
    s = serializer.htmlserializer.HTMLSerializer(omit_optional_tags=False)
    output_generator = s.serialize(stream)

    parts = []
    last_item_was_whitespace = False
    for item in output_generator:
        # Is it empty whitespace?
        if item.strip() != '':
            parts.append(item)
            last_item_was_whitespace = False
        elif not last_item_was_whitespace:
            # Collapse whitespace.
            parts.append(' ')
            last_item_was_whitespace = True
    return ''.join(parts)
    
def are_differences_cosmetic(a, b):
    """
    Returns whether the given strings of HTML are semantically
    identical, assuming whitespace is collapsed.
    """
    
    return _normalize(a) == _normalize(b)
