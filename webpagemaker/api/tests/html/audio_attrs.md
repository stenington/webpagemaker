We want to allow attributes in the `audio`
element, so that people can use audio elements
in their thimble pages

## Input

```html
<!DOCTYPE html><html><head></head><body>
<audio autoplay controls loop="" preload="" src="video.mp3"></audio>
</body></html>
```

## Expected Sanitizer Output

```html
<!DOCTYPE html><html><head></head><body>
<audio autoplay controls loop="" preload="" src="video.mp3"></audio>
</body></html>
```
