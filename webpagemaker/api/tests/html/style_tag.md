We want to allow users to play with CSS, which means we need to allow
use of the `<style>` tag. HTML like this should be perfectly fine:

```html
<!DOCTYPE html><html><head></head><body>
<style>
body {
  background: url(http://test.com/test.jpg);
}
</style>
</body></html>
```
