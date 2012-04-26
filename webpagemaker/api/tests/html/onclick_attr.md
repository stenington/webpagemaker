## Input

```html
<!DOCTYPE html><html><head></head><body>
<a onclick="foo()">u</a>
</body></html>
```

## Expected Sanitizer Output

```html
<!DOCTYPE html><html><head></head><body>
<a>u</a>
</body></html>
```

Note that the `onclick` attribute has been removed to avoid a security breach.
