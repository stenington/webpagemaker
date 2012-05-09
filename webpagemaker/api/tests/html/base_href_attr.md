We want to allow `<base>` tags with the `href` attribute, so that mission
authors can easily fix up their missions to work in WPM. See [#54][] for
more information.

```html
<!DOCTYPE html><html><head>
  <base href="http://foo.com/">
</head><body>
</body></html>
```

  [#54]: https://github.com/mozilla/webpagemaker/issues/54
