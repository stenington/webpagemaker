We want to allow normal links in the pages users write, but we want to
add `rel="nofollow"` to them to make sure that our app can't be used
as a [link farm](http://en.wikipedia.org/wiki/Link_farm).

## Input

```html
<!DOCTYPE html><html><head></head><body>
<a href="http://foo.com/">hi</a>
</body></html>
```

## Expected Sanitizer Output

```html
<!DOCTYPE html><html><head></head><body>
<a href="http://foo.com/" rel="nofollow">hi</a>
</body></html>
```
