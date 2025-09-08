"""
Data loading utilities for posts and publications.
"""
import json
import re
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from .config import POSTS_SRC


def parse_tex_filename(tex_path: Path) -> Tuple[str, str]:
    """Parse YYYY-MM-DD-slug.tex filename format."""
    base = tex_path.stem
    match = re.match(r"(\d{4}-\d{2}-\d{2})-(.+)", base)
    if match:
        return match.group(1), match.group(2)
    return datetime.date.today().isoformat(), base


def read_metadata(slug: str) -> Dict[str, Any]:
    """Read metadata from .meta.json file."""
    meta_path = POSTS_SRC / f"{slug}.meta.json"
    if meta_path.exists():
        with open(meta_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def get_all_posts() -> List[Dict[str, Any]]:
    """Get all blog posts with metadata."""
    posts = []
    for tex_file in POSTS_SRC.glob("*.tex"):
        date_str, slug = parse_tex_filename(tex_file)
        meta = read_metadata(slug)
        
        # Only include if HTML output exists
        html_path = POSTS_SRC / slug / "index.html"
        if html_path.exists():
            # Check if PDF exists
            has_pdf = False
            possible_pdf_names = [
                f"{date_str}-{slug}.pdf",
                f"{slug}.pdf",
                f"2025-09-06-template.pdf" if slug == "template" else None
            ]
            for pdf_name in possible_pdf_names:
                if pdf_name and (POSTS_SRC / pdf_name).exists():
                    has_pdf = True
                    break
            
            posts.append({
                "date": date_str,
                "slug": slug,
                "title": meta.get("title", slug.replace("-", " ").title()),
                "tags": meta.get("tags", []),
                "abstract": meta.get("abstract", ""),
                "has_pdf": has_pdf
            })
    
    # Sort by date (newest first)
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def get_publications() -> List[Dict[str, Any]]:
    """Get all publications from metadata files."""
    publications = []
    pub_dir = Path("publications/data")
    
    if pub_dir.exists():
        for meta_file in pub_dir.glob("*.meta.json"):
            # Skip talks.meta.json as it's handled separately
            if meta_file.name == "talks.meta.json":
                continue
            with open(meta_file, "r", encoding="utf-8") as f:
                pub_data = json.load(f)
                publications.append(pub_data)
    
    # Sort by year (newest first)
    publications.sort(key=lambda p: int(p.get("year", "0")), reverse=True)
    return publications


def get_talks() -> List[Dict[str, Any]]:
    """Get all talks from talks metadata file."""
    talks = []
    talks_file = Path("publications/data/talks.meta.json")
    
    if talks_file.exists():
        with open(talks_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            talks = data.get("talks", [])
    
    # Sort by year (newest first)
    talks.sort(key=lambda t: int(t.get("year", "0")), reverse=True)
    return talks


def copy_blog_posts(posts: List[Dict[str, Any]]) -> None:
    """Blog posts are already in place - no copying needed."""
    print("  📄 Blog posts are already in place in posts/ directory")


def copy_pdf_files(posts: List[Dict[str, Any]]) -> None:
    """PDF files are already in place - no copying needed."""
    print("  📄 PDF files are already in place in posts/ directory")
