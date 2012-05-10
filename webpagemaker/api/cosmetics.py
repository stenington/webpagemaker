"""
    Bleach sanitization changes HTML in ways that are fine for delivering
    raw HTML to a browser, but which can be confusing to the authors
    who wrote the original HTML--particularly when the sanitized HTML
    is semantically unchanged from the original HTML. Examples include the
    removal of whitespace and re-ordering of element attributes.
    
    In the cases where authors have already written sanitized HTML--which
    a nice front-end can help them do--we should be able to re-deliver
    the original HTML they wrote, rather than giving them mangled yet
    semantically-identical HTML. This module provides logic to enable
    us to do this.
    
    For more information and discussion, see:
    
    https://github.com/mozilla/webpagemaker/issues/55
"""

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

    # TODO: We're not actually collapsing *all* whitespace; only
    # entire chunks of whitespace that the serializer gives us. Currently,
    # this seems "good enough" to pass our unit tests, which are
    # based on use cases of comparing pre-sanitized HTML to sanitized HTML,
    # but we may need to change this in the future.
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
