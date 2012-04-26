This directory contains sanitization and idempotency tests, used to verify
that the Webpagemaker API is sanitizing potentially dangerous HTML when
needed, while ensuring that harmless HTML isn't unnecessarily altered.

Roughly speaking, each test is a directory that contains a file called
`in.html`, and an optional file called `out.html`. The first file contains
the input to the API's HTML sanitizer, while the second file, if it exists,
is compared to the sanitizer's output. (If `out.html` doesn't exist, then
the sanitizer's output is compared to the original input.) If the sanitizer's 
output is not identical to the expected output, the test fails.

For example, `script_tag/in.html` contains the following:

```html
<!DOCTYPE html><html><head></head><body>
<script>alert('yo');</script>
</body></html>
```

This HTML will be passed through the sanitizer and compared to `script_tag/out.html`, which contains the following:

```html
<!DOCTYPE html><html><head></head><body>
alert('yo');
</body></html>
```

Notice that the `<script>` tags have been removed in the expected output
to avoid a security breach. If the sanitizer's output doesn't exactly
match the above HTML, however, something is wrong and the test fails.

For more information on the structure of these tests, see
[test_sanitize.py](https://github.com/mozilla/webpagemaker/blob/development/webpagemaker/api/tests/test_sanitize.py#L1).
