# Academic Portfolio

A professional academic portfolio website with clean, modern design.

## Features

- **Professional Academic Design**: Clean, modern layout optimized for academic portfolios
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Automatic Content Integration**: Pulls articles and publications from your existing content
- **Interactive Elements**: Expandable article lists and smooth transitions

## Quick Start

1. **View Your Portfolio**: Open `index.html` in a web browser
2. **Generate Updated Portfolio**: Run `python script/generate_index.py` to update with new content

## Files Structure

```
├── index.html                 # Main portfolio page (GitHub Pages entry point)
├── asset/
│   └── main.css              # Base styles
├── script/
│   ├── generate_index.py     # Portfolio generator
│   └── generate_publications.py     # Publication scanner
├── build/                    # Generated content
└── posts/                    # Your articles
```

## Content Management

The portfolio automatically pulls content from:

- **Articles**: Located in `posts/` directory with `.tex` files
- **Publications**: Located in `Notes/publication/` directory with `.pdf` files
- **Metadata**: Uses `.meta.json` files for article titles and tags

## Deployment

### GitHub Pages

1. Push your repository to GitHub
2. Enable GitHub Pages in repository settings
3. Set source to "Deploy from a branch" and select "main"
4. Your portfolio will be available at `https://yourusername.github.io/your-repo-name`

### Local Development

1. Open `index.html` in a web browser
2. Run `python script/generate_index.py` to update content
3. Refresh the browser to see updates

## Customization

To customize the portfolio:

1. Edit the content directly in `index.html`
2. Modify the `script/generate_index.py` file to change the generation logic
3. Update the CSS styles in the `<style>` section of `index.html`

## Technical Details

- **HTML5**: Semantic markup for accessibility
- **CSS3**: Modern styling with flexbox and grid
- **JavaScript**: Minimal JavaScript for interactivity
- **Python**: Content generation system
- **Responsive**: Mobile-first responsive design

## Browser Support

- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+

## License

This project is open source. Feel free to modify and use for your own academic portfolio.
