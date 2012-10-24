"use strict";

defineTests([
  "thimble/html-badges",
  "backbone-events",
  "slowparse/slowparse"
], function(HTMLBadges, BackboneEvents, Slowparse) {
  module("thimble/html-badges");
  
  function HTMLBadgeTest(name, options) {
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
    
      HTMLBadges.attachProbes(parsingCodeMirror, function credit(behavior) {
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

  HTMLBadgeTest("valid hyperlinks are credited", {
    beginHTML: '<p>hello</p>',
    endHTML: '<p>hello <a href="http://foo.org">there</a></p>',
    credits: ['HYPERLINK']
  });
  
  HTMLBadgeTest("empty hyperlinks are not credited", {
    beginHTML: '<p>hello</p>',
    endHTML: '<p>hello <a href="http://foo.org"></a></p>'
  });

  HTMLBadgeTest("hyperlinks w/ invalid hrefs are not credited", {
    beginHTML: '<p>hello</p>',
    endHTML: '<p>hello <a href="blarg">there</a></p>'
  });
  
  HTMLBadgeTest("non-empty HTML comments are credited", {
    beginHTML: '<p>hello</p>',
    endHTML: '<p>hello <!-- comment --></p>',
    credits: ['HTML_COMMENT']
  });
  
  HTMLBadgeTest("empty HTML comments are not credited", {
    beginHTML: '<p>hello</p>',
    endHTML: '<p>hello <!--  --></p>'
  });
  
  HTMLBadgeTest("changed CSS is credited", {
    beginHTML: '<style>#foo { color: pink; }</style>',
    endHTML: '<style>#foo { color: red; }</style>',
    credits: ['CSS_CHANGED']
  });
  
  HTMLBadgeTest("empty style elements are not credited", {
    beginHTML: '<p>hi</p>',
    endHTML: '<style></style><p></p>'
  });
  
  HTMLBadgeTest("valid iframes are credited", {
    beginHTML: '<p>hi</p>',
    endHTML: '<p>hi <iframe src="http://foo.org/"></iframe></p>',
    credits: ['IFRAME']
  });
  
  HTMLBadgeTest("iframes w/ invalid src attrs are not credited", {
    beginHTML: '<p>hi</p>',
    endHTML: '<p>hi <iframe src="blarg"></iframe></p>',
  });

  HTMLBadgeTest("iframes w/o any src attr are not credited", {
    beginHTML: '<p>hi</p>',
    endHTML: '<p>hi <iframe></iframe></p>',
  });

  HTMLBadgeTest("changing body of an iframe doesn't credit", {
    beginHTML: '<p>hi <iframe src="http://foo.org/"></iframe></p>',
    endHTML: '<p>hi <iframe src="http://foo.org/">lol</iframe></p>'
  });
  
  HTMLBadgeTest("valid images are credited", {
    beginHTML: '<p>hi</p>',
    endHTML: '<p>hi <img src="http://foo.org/"></p>',
    credits: ['IMAGE']
  });
  
  HTMLBadgeTest("images w/o src attrs are not credited", {
    beginHTML: '<p>hi</p>',
    endHTML: '<p>hi <img></p>',
  });

  HTMLBadgeTest("valid ordered lists are credited", {
    beginHTML: '<p>hi <ol></ol></p>',
    endHTML: '<p>hi <ol><li>sup</li></ol></p>',
    credits: ['LIST']
  });

  HTMLBadgeTest("valid unordered lists are credited", {
    beginHTML: '<p>hi <ul></ul></p>',
    endHTML: '<p>hi <ul><li>sup</li></ul></p>',
    credits: ['LIST']
  });

  HTMLBadgeTest("empty list elements are not credited", {
    beginHTML: '<p>hi <ol></ol></p>',
    endHTML: '<p>hi <ol><li></li></ol></p>'
  });

  HTMLBadgeTest("orphan list elements are not credited", {
    beginHTML: '<p>hi</p>',
    endHTML: '<p>hi <li>sup</li></p>'
  });
});
