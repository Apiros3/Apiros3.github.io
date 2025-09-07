# CSS and Code Organization

This document describes the new organized structure for the academic portfolio website.

## CSS Organization

### File Structure
```
css/
├── main.css          # Main CSS file that imports all others
├── base.css          # Base styles, variables, and typography
├── layout.css        # Layout components (header, footer, navigation)
├── components.css    # Reusable components (buttons, cards, etc.)
└── markdown.css      # Markdown content styling
```

### CSS Files

#### `css/main.css`
- Main entry point that imports all other CSS files
- Contains global styles and print/dark mode support
- Imports: base.css, layout.css, components.css, markdown.css

#### `css/base.css`
- CSS custom properties (variables) for consistent theming
- Base typography and element styles
- Utility classes for common patterns
- Math-friendly theorem blocks

#### `css/layout.css`
- Site header, footer, and navigation
- Hero sections
- Main layout grid system
- Responsive design breakpoints

#### `css/components.css`
- Reusable UI components
- Button styles and variants
- Card layouts
- Post and publication item styles
- Filter components
- Form elements

#### `css/markdown.css`
- Styling for markdown content
- Math rendering support
- Code highlighting
- Image and table styling

## Python Code Organization

### File Structure
```
script/
├── __init__.py           # Package initialization
├── config.py             # Configuration settings
├── data_loader.py        # Data loading utilities
├── template_engine.py    # HTML template generation
├── page_generators.py    # Page-specific generators
├── generate_site.py      # Original monolithic generator
└── generate_site_new.py  # New modular generator
```

### Python Modules

#### `script/config.py`
- Centralized configuration settings
- Directory paths and file locations
- Site metadata and branding
- External dependencies (KaTeX, etc.)
- Navigation configuration

#### `script/data_loader.py`
- Functions for loading posts and publications
- Metadata parsing and validation
- File copying utilities
- Data processing and sorting

#### `script/template_engine.py`
- HTML template generation functions
- Reusable template components
- Navigation and layout helpers
- Math rendering configuration

#### `script/page_generators.py`
- Page-specific generation functions
- Main index page generator
- Blog listing page generator
- Publications page generator

## Benefits of New Organization

### CSS Benefits
1. **Modularity**: Each CSS file has a specific purpose
2. **Maintainability**: Easy to find and modify specific styles
3. **Reusability**: Components can be easily reused
4. **Consistency**: CSS variables ensure consistent theming
5. **Performance**: Better caching and loading strategies

### Python Benefits
1. **Separation of Concerns**: Each module has a single responsibility
2. **Testability**: Individual modules can be tested independently
3. **Reusability**: Functions can be imported and reused
4. **Maintainability**: Easier to understand and modify
5. **Extensibility**: New features can be added without affecting existing code

## Migration Notes

### CSS Migration
- All inline styles have been moved to appropriate CSS files
- Duplicate CSS files have been removed
- Template references updated to use new CSS structure
- Legacy `asset/main.css` now imports the new main CSS

### Python Migration
- Original `generate_site.py` preserved for compatibility
- New modular system available in `generate_site_new.py`
- All functionality maintained while improving organization
- Configuration centralized in `config.py`

## Usage

### Using New CSS Structure
All templates now reference `css/main.css` which automatically imports all necessary styles.

### Using New Python Structure
```python
# Import the new generator
from script.generate_site_new import main

# Run the generator
main()
```

### Configuration
Edit `script/config.py` to modify:
- Site title and metadata
- Directory paths
- Navigation items
- External dependencies
- Styling variables

## Future Enhancements

1. **CSS Preprocessing**: Add Sass/SCSS support
2. **Component Library**: Create a formal component library
3. **Theme System**: Implement multiple theme support
4. **Build System**: Add webpack or similar build tools
5. **Testing**: Add unit tests for Python modules
6. **Documentation**: Generate API documentation
