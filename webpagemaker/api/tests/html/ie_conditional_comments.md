## Input

We don't want [Internet Explorer Conditional Comments][iecc] to be able to
trigger arbitrary code for IE users.

Right now we'll just blacklist the `[` and `]`, converting them to
`{` and `}` in an attempt to maintain the semantics of whatever the
comment is trying to communicate.

In the future, an alternative may be to specifically look for IE conditional
comments, rather than blacklisting square brackets entirely.

  [iecc]: http://en.wikipedia.org/wiki/Conditional_comment

```html
<!DOCTYPE html><html><head></head><body>
<!--[if gte IE 4]>
<SCRIPT>alert('XSS');</SCRIPT>
<![endif]-->
</body></html>
```

## Expected Sanitizer Output

```html
<!DOCTYPE html><html><head></head><body>
<!--{if gte IE 4}>
<SCRIPT>alert('XSS');</SCRIPT>
<!{endif}-->
</body></html>
```
