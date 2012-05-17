We want to allow `http` links.

## Input

```html
<!DOCTYPE html><html><head></head><body>
<a href="http://foo.com/">hi</a>
</body></html>
```

## Expected Sanitizer Output

```html
<!DOCTYPE html><html><head></head><body>
<a href="http://foo.com/">hi</a>
</body></html>
```
