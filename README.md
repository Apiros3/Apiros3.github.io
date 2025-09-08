# Apiros3 Homepage + Web Template

A build system for generating an academic portfolio website from TeX files and metadata, with a flexible metafile configuration system.

### Linux/macOS (Make)
```bash
make all
```
## Project Structure

```
├── index.html                 # Main homepage (GitHub Pages entry point)
├── site.meta.json            # Site configuration metafile
├── posts/                     # Blog posts and generated files
│   ├── index.html            # Blog listing page
│   ├── posts/                # Individual blog posts
│   │   ├── [blog-title]/
│   │   └── ...
│   └── pdf/                  # PDF files
├── posts/                    # TeX source files
│   ├── [yyyy]-[mm]-[dd]-[blog-title].tex
│   └── ...
├── publications/              # Publications and talks
│   ├── index.html
│   ├── data/                 # Publication metadata
│   │   ├── [publication].meta.json
│   │   └── talks.meta.json
│   └── scripts/              # Publication generation scripts
├── Notes/                    # Academic notes and papers
│   ├── publication/          # Publication metadata
│   └── [various subjects]/   # Subject-specific notes
├── templates/                # HTML templates
├── script/                   # Python generation scripts
│   ├── config.py            # Metafile configuration loader
│   ├── page_generators.py   # Page generation logic
│   └── generate_site_new.py # Main site generation script
├── css/                      # Stylesheets
├── images/                   # Images and assets
├── build_html.sh            # TeX to HTML conversion
├── Makefile                 # Make-based build system
└── README.md                # This file
```

## Build System Components

### 1. TeX to HTML Conversion
- **Script**: `build_html.sh` (TeX to HTML conversion)
- **Input**: TeX files in `posts/` directory
- **Output**: HTML files in `posts/` directory
- **Tool**: Pandoc for conversion

### 2. Blog Listing Generation
- **File**: `posts/index.html`
- **Features**: Tag filtering, clickable articles, abstracts
- **Data Source**: TeX files and metadata

### 3. Publications Page
- **File**: `publications/index.html`
- **Data Source**: `publications/data/*.meta.json` files
- **Features**: Rich metadata display, multiple link types

### 4. Main Homepage
- **File**: `index.html`
- **Purpose**: GitHub Pages entry point
- **Features**: Recent articles, contact info, navigation
- **Configuration**: Controlled by `site.meta.json`

## Site Configuration System

The site uses a flexible metafile system that allows you to configure your homepage without editing Python code directly.

### Configuration File: `site.meta.json`

#### Site Information
```json
{
  "site": {
    "title": "Apiros3",
    "description": "Academic Portfolio", 
    "author": "Apiros3"
  }
}
```

#### About Section
```json
{
  "about": {
    "title": "About Me",
    "content": "Your about section content here...\n\nYou can write multiple paragraphs by using double line breaks (\\n\\n) in your JSON content. Each paragraph will be automatically wrapped in <p> tags.\n\nThis makes it easy to format longer about sections with proper paragraph breaks."
  }
}
```

#### Contact Information
```json
{
  "contact": {
    "email": "your.email@institution.edu",
    "institution": "[Your Institution]",
    "department": "Mathematics & Computer Science",
    "location": "[Your Location]"
  }
}
```

### Updating Site Configuration

1. **Edit the metafile**: Modify `site.meta.json` with your desired content
2. **Regenerate the site**: Run the site generation script
   ```bash
   # In WSL (recommended)
   wsl python3 script/generate_site_new.py
   
   # Or in PowerShell
   python script/generate_site_new.py
   ```
3. **View changes**: The `index.html` file will be automatically updated

### Multiple Paragraphs in About Content

You can write multiple paragraphs in your about section by using double line breaks (`\n\n`) in your JSON content. Each paragraph will be automatically wrapped in `<p>` tags:

```json
{
  "about": {
    "title": "About Me",
    "content": "First paragraph of your about section.\n\nSecond paragraph with more details.\n\nThird paragraph with additional information."
  }
}
```

This will render as three separate paragraphs in the HTML output.

## Adding New Content

### Adding a New Blog Post

1. **Create TeX file** in `posts/` directory:
   ```bash
   # Format: YYYY-MM-DD-topic.tex
   posts/2025-12-01-new-topic.tex
   ```

2. **Create metadata file**:
   ```json
   {
     "title": "Your Article Title",
     "date": "2025-12-01",
     "tags": ["mathematics", "analysis"],
     "abstract": "Brief description of the article..."
   }
   ```

### Adding a New Publication

1. **Create metadata file** in `publications/data/`:
   ```json
   {
     "title": "Your Paper Title",
     "authors": ["Author One", "Author Two"],
     "conference": "Conference Name",
     "year": "2025",
     "abstract": "Abstract text...",
     "arxiv": "https://arxiv.org/abs/...",
     "doi": "https://doi.org/...",
     "code": "https://github.com/...",
     "venue": "CONF 2025",
     "pages": "1-10"
   }
   ```

2. **Add PDF file**:
   ```bash
   publications/data/your-paper.pdf
   ```

### Talks Metafile

```json
    {
      "title": "Talk Title",
      "type": "workshop / seminar / conference / invited",
      "venue": "Venue",
      "location": "Location",
      "date": "yyyy-mm-dd",
      "year": "yyyy",
      "slides": "link to slides",
      "video": "link to video",
      "abstract": "Abstract text...",
      "coauthors": ["Author one", "Author two"]
    }
```