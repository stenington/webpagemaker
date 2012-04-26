## SKIP THIS TEST

We're not sure if making this test pass is the responsibility of bleach
or our own sanitization code. Until we figure that out, we're skipping
this test.

## Input

```html
I have no doctype.
```

## Expected Sanitizer Output

```html
<!DOCTYPE html><html><head></head><body>I have no doctype.</body></html>
```
