# Thimble Pages

## Style guide

This is an experiment to try out the usefulness of a site style guide. It should be useful to:

  * give the designer a sense of reusable style pieces and a picture of the overall aesthetic
  * give developers an introduction to how the CSS is intended to be used
  * act as a demonstration of the stylesheets in action

## Technical info

The Thimble site styles (*not* the editor!) make use of `sandstone.css` pulled from [bedrock][bedrock], as an
attempt to be resourceful and generally keep in line with the [Mozilla Sandstone look][sandstone].
That in turn seems to mash together some features of the [Less framework][less] with [Twitter Bootstrap][bootstrap].
It's all a bit odd.

[bedrock]: https://github.com/mozilla/bedrock/tree/master/media/css/sandstone
[sandstone]: https://www.mozilla.org/b/en-US/sandstone/
[less]: http://lessframework.com/
[bootstrap]: http://twitter.github.com/bootstrap/

### Build

There is none!

`sandstone.css` was compiled and copied over; updating it would mean doing that again manually. The site-specific css
is written as straight css. Nothing super exciting here.

### Helpful hints

Bootstrap's grid is nicer than Less, imo. Twelve divides nicely by three.

Everything should line up with the *Less Framework 4 grid* preset on [javascriptgrid.org][jsgrid]. Super handy!

[jsgrid]: http://javascriptgrid.org/