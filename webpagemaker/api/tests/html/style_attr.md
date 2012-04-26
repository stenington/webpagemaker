## SKIP THIS TEST

It seems that bleach doesn't sanitize `<style>` tags at all, yet it requires
a whitelist of CSS properties when the `style` *attribute* is allowed. We'll
skip this test until we figure out exactly how to deal with this.

We want to allow users to play with CSS, which means we need to allow
use of the `style` attribute. HTML like this should be perfectly fine:

```html
<!DOCTYPE html><html><head></head><body>
<a style="color: blue">u</a>
<footer style="background: yellow">sup</footer>
</body></html>
```
