We want to ensure that any content we deliver has an HTML5 doctype.

## Input

```html
I have no doctype.
```

## Expected Sanitizer Output

```html
<!DOCTYPE html><html><head></head><body>I have no doctype.</body></html>
```
