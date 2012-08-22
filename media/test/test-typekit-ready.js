defineTests(["thimble/typekit-ready"], function(TypekitReady) {
  module("thimble/typekit-ready");
  
  test("calls onLoad when exception is thrown", function() {
    TypekitReady.load(null, null, function(msg) {
      equal(msg.indexOf('ERROR:'), 0, "msg starts with 'ERROR:'");
    }, {Typekit: null});
  });
  
  test("calls onLoad when Typekit is active", function() {
    TypekitReady.load(null, null, function(msg) {
      equal(msg, "Typekit active");
    }, {
      Typekit: {
        load: function(options) {
          options.active();
        }
      }
    });
  });

  test("calls onLoad when Typekit is inactive", function() {
    TypekitReady.load(null, null, function(msg) {
      equal(msg, "Typekit inactive");
    }, {
      Typekit: {
        load: function(options) {
          options.inactive();
        }
      }
    });
  });  
});
