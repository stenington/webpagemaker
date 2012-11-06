We want to allow attributes in the `video`
element, so that people can use video elements
in their thimble pages

## Input

```html
<!DOCTYPE html><html><head></head><body>
<video autoplay controls height="100px" loop="" muted="" poster="placeholder.gif" preload="" src="video.mp4" width="100px"></video>
</body></html>
```

## Expected Sanitizer Output

```html
<!DOCTYPE html><html><head></head><body>
<video autoplay controls height="100px" loop="" muted="" poster="placeholder.gif" preload="" src="video.mp4" width="100px"></video>
</body></html>
```
