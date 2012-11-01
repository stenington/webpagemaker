"use strict";

defineTests([
  "thimble/html-behaviors",
  "backbone-events",
  "slowparse/slowparse"
], function(Behaviors, BackboneEvents, Slowparse) {
  module("thimble/html-behaviors");
  
  function HTMLBehaviorTest(name, options) {
    test(name, function() {
      var expectedCredits = options.credits || [];
      var originalHTML = options.beginHTML;
      var modifiedHTML = options.endHTML;
      var currentHTML = originalHTML;
      var credits = [];
      var parsingCodeMirror = BackboneEvents.mixin({
        getValue: function() {
          return currentHTML;
        }
      });
    
      Behaviors.attachProbes(parsingCodeMirror, function credit(behavior) {
        credits.push(behavior);
      });

      ok(originalHTML != modifiedHTML,
         "begin snippet (" + parsingCodeMirror.getValue() +
         ") is different from end snippet");

      currentHTML = modifiedHTML;
      var result = Slowparse.HTML(document, parsingCodeMirror.getValue());

      ok(!result.error,
         "end snippet has no errors: " + parsingCodeMirror.getValue());
      parsingCodeMirror.trigger('reparse', result);
      deepEqual(credits, expectedCredits,
                expectedCredits.length ? 
                "behavior(s) " + expectedCredits.join(', ') + " credited" :
                "no behaviors are credited");
    });
  }

  HTMLBehaviorTest("valid hyperlinks are credited", {
    beginHTML: '<p>hello</p>',
    endHTML: '<p>hello <a href="http://foo.org">there</a></p>',
    credits: ['HYPERLINK']
  });
  
  HTMLBehaviorTest("empty hyperlinks are not credited", {
    beginHTML: '<p>hello</p>',
    endHTML: '<p>hello <a href="http://foo.org"></a></p>'
  });

  HTMLBehaviorTest("hyperlinks w/ invalid hrefs are not credited", {
    beginHTML: '<p>hello</p>',
    endHTML: '<p>hello <a href="blarg">there</a></p>'
  });
  
  HTMLBehaviorTest("non-empty HTML comments are credited", {
    beginHTML: '<p>hello</p>',
    endHTML: '<p>hello <!-- comment --></p>',
    credits: ['HTML_COMMENT']
  });
  
  HTMLBehaviorTest("empty HTML comments are not credited", {
    beginHTML: '<p>hello</p>',
    endHTML: '<p>hello <!--  --></p>'
  });
  
  HTMLBehaviorTest("changed CSS in style elements is credited", {
    beginHTML: '<style>#foo { color: pink; }</style>',
    endHTML: '<style>#foo { color: red; }</style>',
    credits: ['CSS_CHANGED']
  });

  HTMLBehaviorTest("changed CSS in style attributes is credited", {
    beginHTML: '<span>hi</span>',
    endHTML: '<span style="color: blue">hi</span>',
    credits: ['CSS_CHANGED']
  });

  HTMLBehaviorTest("empty style attributes are not credited", {
    beginHTML: '<span>hi</span>',
    endHTML: '<span style="">hi</span>'
  });
  
  HTMLBehaviorTest("empty style elements are not credited", {
    beginHTML: '<p>hi</p>',
    endHTML: '<style></style><p></p>'
  });
  
  HTMLBehaviorTest("valid iframes are credited", {
    beginHTML: '<p>hi</p>',
    endHTML: '<p>hi <iframe src="http://foo.org/"></iframe></p>',
    credits: ['IFRAME']
  });
  
  HTMLBehaviorTest("iframes w/ invalid src attrs are not credited", {
    beginHTML: '<p>hi</p>',
    endHTML: '<p>hi <iframe src="blarg"></iframe></p>',
  });

  HTMLBehaviorTest("iframes w/o any src attr are not credited", {
    beginHTML: '<p>hi</p>',
    endHTML: '<p>hi <iframe></iframe></p>',
  });

  HTMLBehaviorTest("changing body of an iframe doesn't credit", {
    beginHTML: '<p>hi <iframe src="http://foo.org/"></iframe></p>',
    endHTML: '<p>hi <iframe src="http://foo.org/">lol</iframe></p>'
  });
  
  HTMLBehaviorTest("valid images are credited", {
    beginHTML: '<p>hi</p>',
    endHTML: '<p>hi <img src="http://foo.org/"></p>',
    credits: ['IMAGE']
  });
  
  HTMLBehaviorTest("images w/o src attrs are not credited", {
    beginHTML: '<p>hi</p>',
    endHTML: '<p>hi <img></p>',
  });

  HTMLBehaviorTest("valid ordered lists are credited", {
    beginHTML: '<p>hi <ol></ol></p>',
    endHTML: '<p>hi <ol><li>sup</li></ol></p>',
    credits: ['LIST']
  });

  HTMLBehaviorTest("valid unordered lists are credited", {
    beginHTML: '<p>hi <ul></ul></p>',
    endHTML: '<p>hi <ul><li>sup</li></ul></p>',
    credits: ['LIST']
  });

  HTMLBehaviorTest("empty list elements are not credited", {
    beginHTML: '<p>hi <ol></ol></p>',
    endHTML: '<p>hi <ol><li></li></ol></p>'
  });

  HTMLBehaviorTest("orphan list elements are not credited", {
    beginHTML: '<p>hi</p>',
    endHTML: '<p>hi <li>sup</li></p>'
  });
  
  for (var i = 1; i <= 6; i++) {
    HTMLBehaviorTest("valid h" + i + " tags are credited", {
      beginHTML: '<p>hi</p>',
      endHTML: '<h' + i + '>yo</h' + i + '><p>hi</p>',
      credits: ['TEXT']
    });
  }

  HTMLBehaviorTest("changing paragraph text is credited", {
    beginHTML: '<p>hi</p>',
    endHTML: '<p>hi there</p>',
    credits: ['TEXT']
  });
  
  HTMLBehaviorTest("adding a div is credited", {
    beginHTML: '<p>hi</p>',
    endHTML: '<div><p>hi</p></div>',
    credits: ['DIV']
  });
  
  HTMLBehaviorTest("adding an audio tag w/ valid src attr is credited", {
    beginHTML: '<p>hi</p>',
    endHTML: '<p>hi <audio src="http://foo/"></audio></p>',
    credits: ['AUDIO']
  });

  HTMLBehaviorTest("adding an audio tag w/ invalid src attr isn't credited", {
    beginHTML: '<p>hi</p>',
    endHTML: '<p>hi <audio src="gweg"></audio></p>'
  });
  
  HTMLBehaviorTest("adding an audio tag w/ valid source tag is credited", {
    beginHTML: '<p>hi</p>',
    endHTML: '<p>hi <audio><source src="http://foo.org/"></audio></p>',
    credits: ['AUDIO']
  });
});
