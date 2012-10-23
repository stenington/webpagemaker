define(function() {
  var behaviorQueries = {
    HYPERLINK: function(doc) {
      var anchors = doc.querySelectorAll("a");
      var candidates = [];
      
      for (var i = 0; i < anchors.length; i++)
        if ((anchors[i].children.length ||
             anchors[i].textContent.trim()) &&
            anchors[i].hasAttribute('href') &&
            anchors[i].getAttribute('href').match(/^https?:/i))
          // TODO: Check href to make sure entire URL is well-formed.
          candidates.push({
            node: anchors[i],
            start: anchors[i].parseInfo.openTag.start,
            end: anchors[i].parseInfo.closeTag.end
          });
      
      return candidates;
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
