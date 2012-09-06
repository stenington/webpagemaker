We want to allow attributes in the `source`
element, so that people can use compound
`video` and `audio` elements in their thimble
pages

## Input

```html
<!DOCTYPE html><html><head></head><body><audio><source src="file.mp3" type="audio/mp3"></audio><video><source src="file.mp4" type="video/mp3"></video></body></html>
```

## Expected Sanitizer Output

```html
<!DOCTYPE html><html><head></head><body><audio><source src="file.mp3" type="audio/mp3"></audio><video><source src="file.mp4" type="video/mp3"></video></body></html>
```
