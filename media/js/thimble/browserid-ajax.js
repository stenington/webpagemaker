define(function() {
  return function BrowserIDAjax(options) {
    var self = {
      email: options.email,
      csrfToken: options.csrfToken
    };
    
    function updateLoginStatus(req) {
      var info = JSON.parse(req.responseText);
      self.csrfToken = info.csrfToken;
      self.email = info.email;
    }

    navigator.id.watch({
      loggedInUser: email,
      onlogin: function(assertion) {
        var req = new XMLHttpRequest();
        var form = new FormData();
        form.append("assertion", assertion);
        req.open('POST', options.verifyURL);
        req.setRequestHeader("X-CSRFToken", self.csrfToken);
        req.onload = function() {
          if (req.status == 200) {
            updateLoginStatus(req);
            options.onlogin.call(self);
          } else {
            console.log("LOGIN FAIL", req.responseText);
          }
        };
        req.send(form);
      },
      onlogout: function() {
        var req = new XMLHttpRequest();
        req.open('POST', options.logoutURL);
        req.setRequestHeader("X-CSRFToken", self.csrfToken);
        req.onload = function() {
          if (req.status == 200) {
            updateLoginStatus(req);
            options.onlogout.call(self);
          } else {
            console.log("LOGOUT FAIL", req.responseText);
          }
        };
        req.send(null);
      }
    });
  };
});
