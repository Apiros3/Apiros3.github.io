# Color Management Guide

This document explains how to manage colors across the entire website from a single location.

## Centralized Color Variables

All colors are defined in `css/base.css` under the `:root` selector. To change any color across the entire site, simply update the corresponding CSS variable.

### Text Colors
```css
--text-primary: #333333;    /* Main text color */
--text-secondary: #555555;  /* Secondary text color */
--text-muted: #666666;      /* Muted text color */
--text-light: #999999;      /* Light text color */
```

### Theme Colors
```css
--primary: #c4b5fd;         /* Primary theme color */
--primary-dark: #a78bfa;    /* Darker primary color */
--secondary: #a8a0c7;       /* Secondary theme color */
--accent: #c4b5fd;          /* Accent color */
```

### Publication Link Colors
```css
--arxiv-color: #ff6b35;     /* arXiv links */
--doi-color: #007cba;       /* DOI links */
--pdf-color: #28a745;       /* PDF links */
--code-color: #6f42c1;      /* Code links */
--slides-color: #17a2b8;    /* Slides links */
--video-color: #dc3545;     /* Video links */
```

### Talk Colors
```css
--talks-color: #17a2b8;     /* Talk item border and type color */
--talks-bg: #e3f2fd;        /* Talk type background */
```

## How to Change Colors

### 1. Change All Text to Black
Update in `css/base.css`:
```css
--text-primary: #000000;
--text-secondary: #000000;
--text-muted: #000000;
```

### 2. Change Theme Colors
Update in `css/base.css`:
```css
--primary: #your-color;
--primary-dark: #your-darker-color;
```

### 3. Change Publication Link Colors
Update in `css/base.css`:
```css
--arxiv-color: #your-arxiv-color;
--doi-color: #your-doi-color;
--pdf-color: #your-pdf-color;
--code-color: #your-code-color;
--slides-color: #your-slides-color;
--video-color: #your-video-color;
```

## File Structure

- `css/base.css` - Contains all color variables and base styles
- `css/pages.css` - Contains page-specific styles that use the color variables
- `css/main.css` - Imports all CSS files
- `script/page_generators.py` - Generates HTML with CSS classes (no inline styles)

## Benefits

1. **Single Source of Truth**: All colors defined in one place
2. **Easy Maintenance**: Change colors without touching Python code
3. **Consistent Theming**: All pages use the same color variables
4. **No Inline Styles**: Clean separation of concerns
5. **Scalable**: Easy to add new colors or themes

## Usage in CSS

Instead of hardcoded colors, use CSS variables:

```css
/* Bad */
color: #333333;

/* Good */
color: var(--text-primary);
```

## Adding New Colors

1. Add the color variable to `css/base.css` under `:root`
2. Use the variable in `css/pages.css` or other CSS files
3. Update Python generators to use appropriate CSS classes
