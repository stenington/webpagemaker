"use strict";

define(["jquery", "backbone-events"], function($, BackboneEvents) {
  return function BrowserIDAjax(options) {
    var id = options.id || window.navigator.id;
    var network = options.network || $;
    var self = {
      email: options.email || null,
      csrfToken: options.csrfToken,
      id: id
    };

    BackboneEvents.mixin(self);
    
    function post(url, data, eventName) {
      network.ajax({
        type: 'POST',
        url: url,
        headers: {"X-CSRFToken": self.csrfToken},
        dataType: 'json',
        data: data,
        success: function(data) {
          self.csrfToken = data.csrfToken;
          self.email = data.email;
          self.trigger(eventName, self);
        }
      });
    }
    
    id.watch({
      loggedInUser: self.email,
      onlogin: function(assertion) {
        post(options.verifyURL, {assertion: assertion}, 'login');
      },
      onlogout: function() {
        post(options.logoutURL, {}, 'logout');
      }
    });
    
    return self;
  };
});
