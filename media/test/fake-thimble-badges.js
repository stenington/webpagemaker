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
      },
      "CSS_LORD": {
        "name": "CSS Lord",
        "description": "You changed CSS.",
        "criteria": "Can change CSS style elements and/or attribute values.",
        "image": "https://wiki.mozilla.org/images/b/bb/Merit-badge.png",
        "behaviors": [{"name": "CSS_CHANGED", "score": 1}],
        "prerequisites": []
      },
      "PORTAL_BUILDER": {
        "name": "Portal Builder",
        "description": "You added or changed an iframe.",
        "criteria": "Can add or change iframes.",
        "image": "https://wiki.mozilla.org/images/b/bb/Merit-badge.png",
        "behaviors": [{"name": "IFRAME", "score": 1}],
        "prerequisites": []
      },
      "IMAGE_MAKER": {
        "name": "Da Vinci Coder",
        "description": "You added or changed an image.",
        "criteria": "Can add or change img tags.",
        "image": "https://wiki.mozilla.org/images/b/bb/Merit-badge.png",
        "behaviors": [{"name": "IMAGE", "score": 1}],
        "prerequisites": []
      },
      "A_LISTER": {
        "name": "A-Lister",
        "description": "You added or changed a list.",
        "criteria": "Can add or change ol/li/ul elements.",
        "image": "https://wiki.mozilla.org/images/b/bb/Merit-badge.png",
        "behaviors": [{"name": "LIST", "score": 1}],
        "prerequisites": []
      },
      "TYPIST": {
        "name": "Typist",
        "description": "You can type. Awesome.",
        "criteria": "Can add or change heading and paragraph elements.",
        "image": "https://wiki.mozilla.org/images/b/bb/Merit-badge.png",
        "behaviors": [{"name": "TEXT", "score": 1}],
        "prerequisites": []
      },
      "DIVMAKER": {
        "name": "Div Maker",
        "description": "You can make divs.",
        "criteria": "Can add or change div elements.",
        "image": "https://wiki.mozilla.org/images/b/bb/Merit-badge.png",
        "behaviors": [{"name": "DIV", "score": 1}],
        "prerequisites": []
      },
      "AUDIOPHILE": {
        "name": "Audiophile",
        "description": "You can make audio.",
        "criteria": "Can add or change audio elements.",
        "image": "https://wiki.mozilla.org/images/b/bb/Merit-badge.png",
        "behaviors": [{"name": "AUDIO", "score": 1}],
        "prerequisites": []
      }
    }
  });
  return {url: url};
});
