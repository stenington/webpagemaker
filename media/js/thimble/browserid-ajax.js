define(["jquery"], function($) {
  return function BrowserIDAjax(options) {
    var self = {
      email: options.email,
      csrfToken: options.csrfToken
    };
    
    function post(url, data, cb) {
      $.ajax({
        type: 'POST',
        url: url,
        headers: {"X-CSRFToken": self.csrfToken},
        dataType: 'json',
        data: data,
        success: function(data) {
          self.csrfToken = data.csrfToken;
          self.email = data.email;
          cb.call(self);
        }
      });
    }
    
    navigator.id.watch({
      loggedInUser: email,
      onlogin: function(assertion) {
        post(options.verifyURL, {assertion: assertion}, options.onlogin);
      },
      onlogout: function() {
        post(options.logoutURL, {}, options.onlogout);
      }
    });
  };
});
