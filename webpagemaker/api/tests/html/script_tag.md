## Input

```html
<!DOCTYPE html><html><head></head><body>
<script>alert('yo');</script>
</body></html>
```

## Expected Sanitizer Output

```html
<!DOCTYPE html><html><head></head><body>
alert('yo');
</body></html>
```

Note that the `<script>` tags have been removed to avoid a security breach.
