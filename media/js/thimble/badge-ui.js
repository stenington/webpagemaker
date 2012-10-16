define([
  "jquery",
  "clopenbadger/clopenbadger",
  "clopenbadger/test/fake-clopenbadger-server"
], function($, Clopenbadger, FakeServer) {
  var fakeServerURL = "http://fake-clopenbadger";
  
  FakeServer.setup({
    urlPrefix: fakeServerURL,
    availableBadges: {
      "FIRST_LOGIN": {
        "name": "First Login",
        "description": "Like a champion, you logged in...",
        "criteria": "Can log into a site that uses Persona for auth.",
        "image": "https://wiki.mozilla.org/images/b/bb/Merit-badge.png",
        "behavior": "LOGGED_IN",
        "score": 1,
        "prerequisites": []
      },
      "HYPERLINKER": {
        "name": "Hyperlinker",
        "description": "You made links.",
        "criteria": "Can make anchor tags with valid href attributes.",
        "image": "https://wiki.mozilla.org/images/b/bb/Merit-badge.png",
        "behavior": "HYPERLINK",
        "score": 1,
        "prerequisites": []
      }
    }
  });
  
  return function BadgeUI(options) {
    var auth = options.auth;
    var container = options.container;
    var alertContainer = options.alertContainer || $(document.body);
    var alertDisplayTime = options.alertDisplayTime || 2000;
    var self = {
      badger: null,
      credit: function(behavior) {
        if (self.badger)
          self.badger.credit(behavior);
      }
    };
    
    auth.on("login", function() {
      var widget = $('<div class="badge-ui-widget"></div>');
      var unreadCount = $('<div class="badge-ui-unread"></div>')
        .appendTo(widget);
      var badgeList = $('<ul class="badge-ui-badges"></ul>')
        .appendTo(widget);
        
      function refreshBadgeList() {
        var available = self.badger.availableBadges;
        var earned = self.badger.earnedBadges;
        badgeList.empty();
        Object.keys(available).forEach(function(shortname) {
          var badge = available[shortname];
          var item = $('<li></li>').text(badge.name);
          if (shortname in earned)
            item.addClass("badge-ui-earned");
          badgeList.append(item);
        });
      }

      container.empty().append(widget);
      self.badger = Clopenbadger({
        server: fakeServerURL,
        token: auth.clopenbadgerToken,
        email: auth.email
      });
      widget.click(function() {
        $(this).toggleClass("badge-ui-on");
        self.badger.markAllBadgesAsRead();
      });
      self.badger.on("change:unreadBadgeCount", function() {
        unreadCount.text(self.badger.unreadBadgeCount.toString());
      });
      self.badger.on("change:availableBadges", refreshBadgeList);
      self.badger.on("change:earnedBadges", refreshBadgeList);
      self.badger.on("award", function(awards) {
        awards.forEach(function(shortname) {
          var badge = self.badger.availableBadges[shortname];
          var alert = $('<div class="ui-badge-alert"></div>');
          alert.text(badge.name).appendTo(alertContainer);
          setTimeout(function() { alert.remove(); }, alertDisplayTime);
        });
      });
      self.credit("LOGGED_IN");
    }).on("logout", function() {
      container.empty();
      self.badger = null;
    });

    return self;
  };
});
