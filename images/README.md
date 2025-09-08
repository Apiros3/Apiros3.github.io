# Images Directory

This directory contains images for the academic portfolio website.

## Profile Picture

Place your profile picture here as `profile.jpg`. The image should be:
- Square format (recommended: 400x400 pixels or higher)
- Good quality and professional appearance
- JPG, PNG, or WebP format

The profile picture will be automatically styled as a circular image with a border and shadow on the about page.

## Current Configuration

The profile picture is configured in `site.meta.json`:
```json
"about": {
  "profile_picture": "images/profile.jpg",
  "profile_alt": "Tadayoshi Kamegai - Profile Picture"
}
```

To change the profile picture:
1. Replace `images/profile.jpg` with your new image
2. Update the `profile_alt` text in `site.meta.json` if needed
3. Regenerate the site with `make generate`
