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
});
