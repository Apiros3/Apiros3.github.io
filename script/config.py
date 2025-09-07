"""
Configuration settings for the academic portfolio site generator.
"""
from pathlib import Path

# Directory paths
POSTS_SRC = Path("posts")
BUILD = Path("build")
POSTS_OUT = BUILD / "posts"
PDF_OUT = BUILD / "pdf"
TEMPLATES = Path("templates")
CSS_DIR = Path("css")
ASSETS_DIR = Path("asset")

# Site configuration
SITE_TITLE = "Apiros3"
SITE_DESCRIPTION = "Academic Portfolio"
SITE_AUTHOR = "Apiros3"
SITE_EMAIL = "your.email@institution.edu"
SITE_INSTITUTION = "[Your Institution]"
SITE_DEPARTMENT = "Mathematics & Computer Science"
SITE_LOCATION = "[Your Location]"

# CSS files
CSS_FILES = [
    "css/main.css"
]

# External dependencies
KATEX_CSS = "https://cdn.jsdelivr.net/npm/katex/dist/katex.min.css"
KATEX_JS = "https://cdn.jsdelivr.net/npm/katex/dist/katex.min.js"
KATEX_AUTO_RENDER = "https://cdn.jsdelivr.net/npm/katex/dist/contrib/auto-render.min.js"

# Math rendering configuration
MATH_DELIMITERS = [
    {"left": "$$", "right": "$$", "display": True},
    {"left": "\\[", "right": "\\]", "display": True},
    {"left": "$", "right": "$", "display": False},
    {"left": "\\(", "right": "\\)", "display": False}
]

# Navigation configuration
NAV_ITEMS = [
    {"name": "About", "url": "./index.html", "current": False},
    {"name": "Publications", "url": "build/publications.html", "current": False},
    {"name": "Blog", "url": "build/index.html", "current": False}
]

# Publication link colors
PUB_LINK_COLORS = {
    "arxiv": "#ff6b35",
    "doi": "#007cba", 
    "pdf": "#28a745",
    "code": "#6f42c1"
}
