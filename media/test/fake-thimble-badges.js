define([
  "clopenbadger/test/fake-clopenbadger-server"
], function(FakeClopenbadgerServer) {
  var url = "http://fake-clopenbadger";
  FakeClopenbadgerServer.setup({
    urlPrefix: url,
    availableBadges: {
      "FIRST_LOGIN": {
        "name": "First Login",
        "description": "Like a champion, you logged in...",
        "criteria": "Can log into a site that uses Persona for auth.",
        "image": "https://wiki.mozilla.org/images/b/bb/Merit-badge.png",
        "behaviors": [{"name": "LOGGED_IN", "score": 1}],
        "prerequisites": []
      },
      "HYPERLINKER": {
        "name": "Hyperlinker",
        "description": "You made links.",
        "criteria": "Can make anchor tags with valid href attributes.",
        "image": "https://wiki.mozilla.org/images/b/bb/Merit-badge.png",
        "behaviors": [{"name": "HYPERLINK", "score": 1}],
        "prerequisites": []
      },
      "HTML_DOCUMENTER": {
        "name": "HTML Documenter",
        "description": "You made HTML comments.",
        "criteria": "Can make HTML comments.",
        "image": "https://wiki.mozilla.org/images/b/bb/Merit-badge.png",
        "behaviors": [{"name": "HTML_COMMENT", "score": 1}],
        "prerequisites": []
      }
    }
  });
  return {url: url};
});
