Introduction
============

This website represents a sophisticated academic portfolio system built
around a flexible, metadata-driven architecture. The system combines TeX
document processing, Python-based site generation, and modern web
technologies to create a maintainable, professional academic presence.

The core philosophy is *separation of concerns*: content (TeX files),
configuration (JSON metafiles), and presentation (HTML/CSS) are kept
distinct, allowing for easy maintenance and updates without touching the
underlying codebase.

System Architecture Overview
============================

High-Level Architecture
-----------------------

The website follows a three-tier architecture:

1.  **Content Layer**: TeX source files, JSON metadata files, and static
    assets

2.  **Processing Layer**: Python scripts, build tools, and conversion
    pipelines

3.  **Presentation Layer**: Generated HTML, CSS, and JavaScript

Core Components
---------------

The system consists of several key components:

-   **TeX Processing Pipeline**: Converts academic papers and blog posts
    from TeX to HTML

-   **Metafile Configuration System**: Manages site-wide settings and
    content metadata

-   **Page Generation Engine**: Creates HTML pages from templates and
    data

-   **Publication Management**: Handles academic publications and talks

-   **Notes Organization**: Manages academic notes and paper summaries

-   **Reading List System**: Tracks books, papers, and resources

Directory Structure and File Organization
=========================================

Root Directory Structure
------------------------

    Apiros3.github.io/
    |-- index.html                 # Main homepage (GitHub Pages entry)
    |-- site.meta.json            # Site configuration metafile
    |-- posts/                     # Blog posts and TeX sources
    |   |-- index.html            # Blog listing page
    |   |-- [yyyy]-[mm]-[dd]-[title].tex  # TeX source files
    |   `-- [title]/              # Generated blog post directories
    |-- publications/              # Publications and talks
    |   |-- index.html
    |   |-- data/                 # Publication metadata
    |   `-- scripts/              # Generation scripts
    |-- Notes/                    # Academic notes
    |-- templates/                # HTML templates
    |-- script/                   # Python generation system
    |-- css/                      # Stylesheets
    |-- images/                   # Static assets
    |-- build_html.sh            # TeX conversion script
    |-- Makefile                 # Build system
    `-- README.md                # Documentation

Key Configuration Files
-----------------------

A metafile is a JSON configuration file that contains structured data
about content, settings, or metadata. The system uses multiple metafiles
to manage different aspects of the website.

The system uses several metafiles:

-   `site.meta.json`: Main site configuration

-   `notes.meta.json`: Academic notes metadata

-   `reading-list.meta.json`: Reading list data

-   `publications/data/*.meta.json`: Publication metadata

-   `posts/*.meta.json`: Blog post metadata

The TeX Processing Pipeline
===========================

TeX to HTML Conversion
----------------------

The TeX processing pipeline converts academic documents to web-friendly
HTML:

``` {.bash language="bash" caption="TeX conversion process"}
# TeX file naming convention
posts/YYYY-MM-DD-title.tex

# Conversion command (simplified)
pandoc input.tex -o output.html --mathjax --standalone
```

Build Script Architecture
-------------------------

The `build_html.sh` script handles the conversion process:

1.  Scans the `posts/` directory for TeX files

2.  Extracts metadata from TeX headers

3.  Converts each file using Pandoc with appropriate settings

4.  Generates corresponding metadata files

5.  Creates individual blog post directories

6.  Updates the blog listing page

Pandoc Configuration
--------------------

The system uses Pandoc with specific settings optimized for academic
content:

-   Math rendering via MathJax

-   Syntax highlighting for code blocks

-   Cross-reference support

-   Table of contents generation

-   Custom CSS integration

The Metafile Configuration System
=================================

Site Configuration (`site.meta.json`)
-------------------------------------

The main site configuration controls the homepage and global settings:

    {
      "site": {
        "title": "Apiros3",
        "description": "Academic Portfolio",
        "author": "Apiros3"
      },
      "about": {
        "title": "About Me",
        "content": "Multi-paragraph content...",
        "profile_picture": "images/profile.jpg"
      },
      "contact": {
        "email": "email@institution.edu",
        "institution": "University Name",
        "location": "City, Country"
      },
      "navigation": {
        "brand": "Apiros3",
        "items": [...]
      }
    }

Multiple Paragraph Support
--------------------------

The system supports multiple paragraphs in the about section using
double line breaks:

    {
      "about": {
        "content": "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
      }
    }

This is processed by the `format_about_content()` function in
`script/page_generators.py`.

The Python Generation System
============================

Core Modules
------------

The Python system consists of several modules:

-   `config.py`: Configuration loading and management

-   `page_generators.py`: HTML page generation logic

-   `template_engine.py`: Template rendering functions

-   `data_loader.py`: Data loading and processing

-   `generate_site_new.py`: Main orchestration script

Page Generation Process
-----------------------

The page generation follows this workflow:

1.  Load configuration from metafiles

2.  Process TeX files and extract metadata

3.  Load publication and talk data

4.  Generate HTML pages using templates

5.  Apply styling and JavaScript

6.  Output final HTML files

Template System
---------------

The template system uses Python string formatting with custom functions:

``` {language="python" caption="Template function example"}
def generate_html_head(title: str, base_path: str = "") -> str:
    """Generate HTML head section with CSS and metadata."""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>{title}</title>
  <link rel="stylesheet" href="{base_path}css/main.css">
</head>"""
```

Publication Management System
=============================

Publication Data Structure
--------------------------

Publications are managed through JSON metadata files:

    {
      "title": "Paper Title",
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

Talk Management
---------------

Talks follow a similar structure with additional fields:

    {
      "title": "Talk Title",
      "type": "workshop / seminar / conference / invited",
      "venue": "Venue Name",
      "location": "City, Country",
      "date": "2025-09-08",
      "year": "2025",
      "slides": "https://slides.com/...",
      "video": "https://youtube.com/...",
      "abstract": "Talk abstract...",
      "coauthors": ["Author One", "Author Two"]
    }

Notes and Reading List Systems
==============================

Notes Organization
------------------

Academic notes are organized by subject with metadata:

    {
      "title": "Subject Name",
      "description": "Brief description...",
      "pdf_file": "notes.pdf",
      "pdf_files": ["lec1.pdf", "lec2.pdf"],
      "tags": ["mathematics", "analysis"]
    }

Reading List Management
-----------------------

The reading list tracks academic resources:

    {
      "title": "Book/Paper Title",
      "author": "Author Name",
      "year": "2025",
      "type": "book / paper / article",
      "status": "reading / completed / planned",
      "description": "Brief description..."
    }

Build System and Automation
===========================

Makefile Targets
----------------

The Makefile provides several build targets:

``` {.makefile language="make" caption="Makefile targets"}
all: clean blog main pub          # Full build
blog:                            # Blog posts only
main:                           # Main pages only
pub:                            # Publications only
clean:                          # Clean generated files
help:                           # Show help
```

Cross-Platform Support
----------------------

The system supports multiple platforms:

-   **Linux/macOS**: Native Make support

-   **Windows**: Batch files and PowerShell scripts

-   **WSL**: Full Linux compatibility on Windows

CSS and Styling System
======================

CSS Architecture
----------------

The styling system uses a modular CSS approach:

-   `base.css`: Core variables, typography, and base styles

-   `layout.css`: Layout components and responsive design

-   `components.css`: Reusable UI components

-   `pages.css`: Page-specific styles

-   `markdown.css`: Content styling for blog posts

-   `main.css`: Main stylesheet that imports all others

Typography System
-----------------

The system uses a professional typography stack:

``` {.c language="C" caption="Typography configuration"}
:root {
  --font-family: 'Inter', 'Source Sans Pro', 'Segoe UI', system-ui, sans-serif;
  --font-family-mono: 'JetBrains Mono', 'Fira Code', monospace;
  --font-size-base: 16px;
  --line-height-base: 1.7;
}
```

Responsive Design
-----------------

The system implements responsive design principles:

-   Mobile-first approach

-   Flexible grid system

-   Adaptive typography

-   Touch-friendly navigation

Content Management Workflow
===========================

Adding New Blog Posts
---------------------

To add a new blog post:

1.  Create TeX file: `posts/YYYY-MM-DD-title.tex`

2.  Write content using LaTeX syntax

3.  Optionally create metadata file: `posts/title.meta.json`

4.  Run build system: `make all`

Updating Site Configuration
---------------------------

To update site-wide settings:

1.  Edit `site.meta.json`

2.  Modify desired configuration sections

3.  Run site generation: `python script/generate_site_new.py`

4.  Verify changes in generated HTML

Managing Publications
---------------------

To add a new publication:

1.  Create metadata file: `publications/data/paper.meta.json`

2.  Add PDF file if available

3.  Run build system to update publications page

Deployment and Hosting
======================

GitHub Pages Integration
------------------------

The system is designed for GitHub Pages deployment:

1.  Push repository to GitHub

2.  Enable GitHub Pages in repository settings

3.  Set source to \"Deploy from a branch\"

4.  Select main branch and root folder

5.  The `index.html` serves as the entry point

Local Development
-----------------

For local development:

``` {.bash language="bash" caption="Local development commands"}
# View main page
start index.html

# View blog
start posts/index.html

# View publications
start publications/index.html
```

Advanced Features
=================

Tag Filtering System
--------------------

The blog system includes JavaScript-based tag filtering:

-   Automatic tag extraction from TeX metadata

-   Interactive filter buttons

-   Real-time content filtering

-   URL-based filter state management

Math Rendering
--------------

Mathematical content is rendered using MathJax:

-   Inline math: `$...$`

-   Display math: `$$...$$`

-   LaTeX environments support

-   Cross-reference compatibility

Code Highlighting
-----------------

Code blocks are highlighted using Pandoc's syntax highlighting:

-   Language detection

-   Theme customization

-   Copy-to-clipboard functionality

-   Mobile-friendly display

Maintenance and Troubleshooting
===============================

Common Issues
-------------

1.  **Pandoc not found**: Install Pandoc and ensure it's in PATH

2.  **Python errors**: Check Python installation and dependencies

3.  **TeX conversion errors**: Verify LaTeX syntax and packages

4.  **Metafile errors**: Validate JSON syntax

5.  **Missing files**: Run full build system

Debugging Workflow
------------------

When issues arise:

1.  Check build output for error messages

2.  Verify all dependencies are installed

3.  Ensure you're running from project root

4.  Check file permissions and paths

5.  Validate JSON syntax in metafiles

Performance Considerations
==========================

Optimization Strategies
-----------------------

The system implements several optimization strategies:

-   Minified CSS and JavaScript

-   Optimized images and assets

-   Efficient HTML generation

-   Lazy loading for large content

-   CDN integration for external resources

Loading Performance
-------------------

Key performance metrics:

-   Fast initial page load

-   Efficient navigation

-   Quick content filtering

-   Responsive image loading

Future Enhancements
===================

Planned Features
----------------

Potential future improvements:

-   Dark mode support

-   Search functionality

-   RSS feed generation

-   Comment system integration

-   Advanced analytics

Extensibility
-------------

The system is designed for easy extension:

-   Modular architecture

-   Plugin system potential

-   Template customization

-   Theme system

Conclusion
==========

This academic portfolio website represents a sophisticated, maintainable
system for presenting academic work online. The combination of TeX
processing, Python generation, and modern web technologies creates a
flexible platform that can adapt to changing needs while maintaining
professional presentation standards.

The key to the system's success is its *separation of concerns*:
content, configuration, and presentation are kept distinct, allowing for
easy maintenance and updates. The metafile system provides a
user-friendly interface for content management, while the Python
generation system ensures consistency and reliability.

For anyone wishing to understand, modify, or extend this system, this
document provides the comprehensive technical foundation necessary for
effective development and maintenance.
