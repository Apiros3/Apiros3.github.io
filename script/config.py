"""
Configuration settings for the academic portfolio site generator.
"""
import json
from pathlib import Path

# Directory paths
POSTS_SRC = Path("posts")
TEMPLATES = Path("templates")
CSS_DIR = Path("css")
ASSETS_DIR = Path("asset")

# Load site metadata from metafile
def load_site_metadata():
    """Load site metadata from site.meta.json file."""
    try:
        with open("site.meta.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback to default values if metafile doesn't exist
        return {
            "site": {
                "title": "Apiros3",
                "description": "Academic Portfolio", 
                "author": "Apiros3"
            },
            "about": {
                "title": "About",
                "content": "Welcome to my academic portfolio. I am a research scientist working at the intersection of mathematics and computer science. My research focuses on algebraic structures, formal methods, and theoretical computer science, with particular emphasis on the connections between algebra and logic in computational systems."
            },
            "contact": {
                "email": "your.email@institution.edu",
                "institution": "[Your Institution]",
                "department": "Mathematics & Computer Science",
                "location": "[Your Location]"
            },
            "navigation": {
                "brand": "Apiros3",
                "items": [
                    {"name": "About", "url": "./index.html", "current": True},
                    {"name": "Publications", "url": "publications/index.html", "current": False},
                    {"name": "Blog", "url": "posts/index.html", "current": False}
                ]
            },
            "recent_posts": {
                "title": "Recent Blog Posts",
                "limit": 5,
                "show_abstract": False,
                "show_tags": False
            }
        }

# Load metadata
SITE_METADATA = load_site_metadata()

# Site configuration (from metafile)
SITE_TITLE = SITE_METADATA["site"]["title"]
SITE_DESCRIPTION = SITE_METADATA["site"]["description"]
SITE_AUTHOR = SITE_METADATA["site"]["author"]
SITE_EMAIL = SITE_METADATA["contact"]["email"]
SITE_INSTITUTION = SITE_METADATA["contact"]["institution"]
SITE_DEPARTMENT = SITE_METADATA["contact"].get("department", "")
SITE_LOCATION = SITE_METADATA["contact"]["location"]

# About section configuration
ABOUT_TITLE = SITE_METADATA["about"]["title"]
ABOUT_CONTENT = SITE_METADATA["about"]["content"]
ABOUT_PROFILE_PICTURE = SITE_METADATA["about"].get("profile_picture", "")
ABOUT_PROFILE_ALT = SITE_METADATA["about"].get("profile_alt", "Profile Picture")

# Navigation configuration
NAV_BRAND = SITE_METADATA["navigation"]["brand"]
NAV_ITEMS = SITE_METADATA["navigation"]["items"]

# Recent posts configuration
RECENT_POSTS_TITLE = SITE_METADATA["recent_posts"]["title"]
RECENT_POSTS_LIMIT = SITE_METADATA["recent_posts"]["limit"]
RECENT_POSTS_SHOW_ABSTRACT = SITE_METADATA["recent_posts"]["show_abstract"]
RECENT_POSTS_SHOW_TAGS = SITE_METADATA["recent_posts"]["show_tags"]

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


# Publication link colors
PUB_LINK_COLORS = {
    "arxiv": "#ff6b35",
    "doi": "#007cba", 
    "pdf": "#28a745",
    "code": "#6f42c1"
}
