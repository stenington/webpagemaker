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

Everything should line up with the <a href="javascript:(function(){window.javascriptgrid={columns:{'default':{columns:10},a:{minWidth:768,maxWidth:991,columns:8},b:{minWidth:480,maxWidth:767,columns:5},c:{minWidth:1,maxWidth:479,columns:3}},columnWidth:68,gapWidth:24};var%20script=document.createElement('script');script.src='http://jsg.javascriptgrid.org/jsg.js';document.getElementsByTagName('HEAD')%5B0%5D.appendChild(script);})();">Less Framework 4 grid</a> preset on [javascriptgrid.org][jsgrid]. Super handy!

[jsgrid]: http://javascriptgrid.org/