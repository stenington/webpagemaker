"use strict";

define(["jquery", "backbone-events"], function($, BackboneEvents) {
  return function BrowserIDAjax(options) {
    var id = options.id || window.navigator.id;
    var network = options.network || $;
    var self = {
      email: options.email || null,
      csrfToken: options.csrfToken,
      clopenbadgerToken: options.clopenbadgerToken || null,
      id: id,
      login: function() {
        self.id.get(function(assertion) {
          if (assertion)
            post(options.verifyURL, {assertion: assertion}, 'login');
          else
            self.trigger("login:error");
        });
      },
      logout: function() {
        post(options.logoutURL, {}, 'logout');
      }
    };

    BackboneEvents.mixin(self);
    
    function post(url, data, eventName) {
      network.ajax({
        type: 'POST',
        url: url,
        headers: {"X-CSRFToken": self.csrfToken},
        dataType: 'json',
        data: data,
        error: function() {
          self.trigger(eventName + ":error");
        },
        success: function(data) {
          self.csrfToken = data.csrfToken;
          self.email = data.email;
          self.clopenbadgerToken = data.clopenbadgerToken;
          self.trigger(eventName, self);
        }
      });
    }
    
    return self;
  };
});
