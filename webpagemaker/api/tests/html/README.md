This directory contains sanitization and idempotency tests, used to verify
that the Webpagemaker API is sanitizing potentially dangerous HTML when
needed, while ensuring that harmless HTML isn't unnecessarily altered.

The tests are designed to be human-readable. The suite [test_sanitize.py][]
parses them and makes sure the code matches our expectations.

  [test_sanitize.py]: https://github.com/mozilla/webpagemaker/blob/development/webpagemaker/api/tests/test_sanitize.py#L1
