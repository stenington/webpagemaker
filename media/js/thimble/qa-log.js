define([
  "jquery"
], function($) {
  var PROMPT_MSG = [
    "Please enter comments for your feedback below. Note that along with ",
    "your comments, we will include information about your browser and ",
    "other data that will help us debug any problems you may be having. ",
    "If you don't want to do this, just click cancel."
  ].join('');
  var log = [];

  var self = {
    start: Date.now(),
    now: Date.now,
    logBasicInfo: function() {
      self.safely(function(log) {
        log("user-agent", window.navigator.userAgent);
        log("location", window.location.href);
      });
    },
    log: function() {
      var time = self.now() - self.start;
      log.push([time].concat(Array.prototype.slice.call(arguments)));
    },
    safely: function(cb) {
      try {
        cb(self.log);
      } catch (e) {
        var str = "unknown error";
        try {
          str = e.toString();
        } catch (e) {}
        self.log("safely() raised exception", str);
      }
    },
    get: function() {
      return log.slice();
    },
    report: function() {
      var comments = window.prompt(PROMPT_MSG, "");
      if (comments === null)
        return;
      jQuery.ajax({
        type: 'POST',
        url: 'http://hackpub.hackasaurus.org/buckets/webxray-bugs/publish',
        data: {
          'json': JSON.stringify({
            comments: comments || '',
            log: log
          }),
          'original-url': window.location.href
        },
        dataType: 'json',
        crossDomain: true,
        success: function(data) {
          ghettoMessage('Bug report submitted ' +
                        '<a href="' + data['published-url'] + 
                        '">here</a>. Thanks!');
        }
      });
    }
  };

  function ghettoMessage(html) {
    var div = $('<div></div>').appendTo(document.body).css({
      'position': 'absolute',
      'bottom': '0',
      'left': '0',
      'z-index': '1000000',
      'color': 'white',
      'background-color': 'rgba(0, 0, 0, 0.5)',
      'font-size': '30px',
      'font-family': 'Open Sans'
    });
    var closeBox = $('<div>X</div>').appendTo(div).css({
      'display': 'inline-block',
      'padding': '10px',
      'cursor': 'pointer',
      'background-color': 'rgba(255, 255, 255, 0.2)'
    }).click(function() { div.remove(); });
    var message = $('<div></div>').html(html).appendTo(div).css({
      'display': 'inline-block',
      'padding': '4px'
    });
    $('*', message).css({'color': 'white'});
  }
  
  function stripQuery(url) {
    var qsIndex = url.indexOf("?");
    if (qsIndex == -1)
      return url;
    return url.slice(0, qsIndex);
  }
  
  function logWindowErrors() {
    // From https://developer.mozilla.org/en-US/docs/DOM/window.onerror
    var gOldOnError = window.onerror;
    // Override previous handler.
    window.onerror = function myErrorHandler(errorMsg, url, lineNumber) {
      if (gOldOnError)
        // Call previous handler.
        return gOldOnError(errorMsg, url, lineNumber);

      self.log("window.onerror", errorMsg, url, lineNumber);

      // Let default handler run.
      return false;
    }
  }
  
  function logAjax() {
    $(document.body).ajaxError(function(evt, xhr, settings, err) {
      self.log("ajaxError", stripQuery(settings.url), xhr.status, err);
    }).ajaxSuccess(function(evt, xhr, settings) {
      self.log("ajaxSuccess", stripQuery(settings.url), xhr.status);
    });
  }
  
  self.safely(logWindowErrors);
  self.safely(logAjax);
  self.logBasicInfo();
  
  return self;
});
