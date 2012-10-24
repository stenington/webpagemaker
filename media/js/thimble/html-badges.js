define(function() {
  function select(doc, selector) {
    return Array.prototype.slice.call(doc.querySelectorAll(selector));
  }

  function attrHasValidURL(node, attr) {
    // TODO: Check href to make sure entire URL is well-formed.        
    return (node.hasAttribute(attr) &&
            node.getAttribute(attr).match(/^https?:/i));
  }
  
  function candidateFromOpenTag(node) {
    return {
      node: node,
      start: node.parseInfo.openTag.start,
      end: node.parseInfo.openTag.end
    };
  }
  
  function candidateFromElement(node) {
    return {
      node: node,
      start: node.parseInfo.openTag.start,
      end: node.parseInfo.closeTag.end
    };
  }

  function candidateFromAttr(attr) {
    return function(node) {
      for (var i = 0; i < node.attributes.length; i++) {
        var attrNode = node.attributes[i];
        if (attrNode.nodeName.toLowerCase() == attr) {
          return {
            node: node,
            start: attrNode.parseInfo.value.start,
            end: attrNode.parseInfo.value.end
          };
        }
      }
      throw new Error("assertion failure: node does not have '" +
                      attr + "' attribute");
    };
  }
  
  var behaviorQueries = {
    HYPERLINK: function(doc) {
      return select(doc, "a").filter(function(anchor) {
        return ((anchor.children.length ||
                 anchor.textContent.trim()) &&
                 attrHasValidURL(anchor, 'href'));
      }).map(candidateFromElement);
    },
    HTML_COMMENT: function(doc) {
      var candidates = [];
      
      function traverse(element) {
        for (var i = 0; i < element.childNodes.length; i++) {
          var node = element.childNodes[i];
          
          if (node.nodeType == element.ELEMENT_NODE)
            traverse(node);
          else if (node.nodeType == element.COMMENT_NODE &&
                   node.nodeValue.trim())
            candidates.push({
              node: node,
              start: node.parseInfo.start,
              end: node.parseInfo.end
            });
        }
      }
      
      traverse(doc);
      return candidates;
    },
    CSS_CHANGED: function(doc) {
      var styleElements = select(doc, "style").filter(function(style) {
        return (!!style.textContent.trim());
      }).map(candidateFromElement);
      
      var styleAttrs = select(doc, "[style]").filter(function(node) {
        return (!!node.getAttribute("style").trim());
      }).map(candidateFromAttr("style"));
      
      return styleElements.concat(styleAttrs);
    },
    IFRAME: function(doc) {
      return select(doc, "iframe").filter(function(iframe) {
        return attrHasValidURL(iframe, 'src');
      }).map(candidateFromOpenTag);
    },
    IMAGE: function(doc) {
      return select(doc, "img").filter(function(img) {
        return attrHasValidURL(img, 'src');
      }).map(candidateFromOpenTag);
    },
    LIST: function(doc) {
      return select(doc, "li").filter(function(li) {
        return (!!li.textContent.trim() &&
                li.parentNode &&
                (li.parentNode.nodeName == "OL" ||
                 li.parentNode.nodeName == "UL"));
      }).map(candidateFromElement);
    },
    TEXT: function(doc) {
      return select(doc, "h1,h2,h3,h4,h5,h6,p").filter(function(node) {
        return (node.childNodes.length == 1 &&
                node.childNodes[0].nodeType == node.TEXT_NODE &&
                node.childNodes[0].nodeValue.trim());
      }).map(candidateFromElement);
    },
    AUDIO: function(doc) {
      return select(doc, "audio").filter(function(node) {
        if (attrHasValidURL(node, 'src'))
          return true;
        var source = node.querySelector("source");
        return (source && attrHasValidURL(source, 'src'));
      }).map(candidateFromElement);
    },
    DIV: function(doc) {
      return select(doc, "div").filter(function(node) {
        return (!!node.textContent.trim());
      }).map(candidateFromElement);
    }
  };
  
  return {
    attachProbes: function(parsingCodeMirror, credit) {
      var originalCode = parsingCodeMirror.getValue();
      
      parsingCodeMirror.on("reparse", function(event) {
        var currentCode = parsingCodeMirror.getValue();

        if (event.error)
          return;
        
        Object.keys(behaviorQueries).forEach(function(behavior) {
          var candidates = behaviorQueries[behavior](event.document);
          
          candidates.forEach(function(info) {
            var snippet = currentCode.slice(info.start, info.end);
            if (originalCode.indexOf(snippet) == -1) {
              credit(behavior);
              originalCode = currentCode;
              //console.log("credit " + behavior + " for " + snippet);
            }
          });
        });
      });
    }
  };
});
