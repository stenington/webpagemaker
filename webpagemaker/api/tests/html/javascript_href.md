## Input

```html
<!DOCTYPE html><html><head></head><body>
<a href="javascript:foo()">u</a>
</body></html>
```

## Expected Sanitizer Output

```html
<!DOCTYPE html><html><head></head><body>
<a>u</a>
</body></html>
```

Note that the `javascript:` URL is removed from the anchor to avoid a security 
breach.
