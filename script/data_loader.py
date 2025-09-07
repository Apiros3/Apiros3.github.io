"""
Data loading utilities for posts and publications.
"""
import json
import re
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from .config import POSTS_SRC, BUILD


def parse_tex_filename(tex_path: Path) -> tuple[str, str]:
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
            with open(meta_file, "r", encoding="utf-8") as f:
                pub_data = json.load(f)
                publications.append(pub_data)
    
    # Sort by year (newest first)
    publications.sort(key=lambda p: int(p.get("year", "0")), reverse=True)
    return publications


def copy_blog_posts(posts: List[Dict[str, Any]]) -> None:
    """Copy individual blog post HTML files to build directory."""
    POSTS_OUT.mkdir(exist_ok=True)
    
    for post in posts:
        slug = post["slug"]
        src_dir = POSTS_SRC / slug
        dst_dir = POSTS_OUT / slug
        
        if src_dir.exists():
            # Create destination directory
            dst_dir.mkdir(exist_ok=True)
            
            # Copy HTML file
            src_html = src_dir / "index.html"
            if src_html.exists():
                dst_html = dst_dir / "index.html"
                dst_html.write_text(src_html.read_text(encoding="utf-8"), encoding="utf-8")
                print(f"  📄 Copied {slug}/index.html")


def copy_pdf_files(posts: List[Dict[str, Any]]) -> None:
    """Copy PDF files to build directory."""
    PDF_OUT.mkdir(exist_ok=True)
    
    for post in posts:
        slug = post["slug"]
        
        # Look for PDF files with various naming patterns
        possible_pdf_names = [
            f"{post['date']}-{slug}.pdf",
            f"{slug}.pdf",
            f"2025-09-06-template.pdf" if slug == "template" else None
        ]
        
        pdf_found = False
        for pdf_name in possible_pdf_names:
            if pdf_name and (POSTS_SRC / pdf_name).exists():
                src_pdf = POSTS_SRC / pdf_name
                dst_pdf = PDF_OUT / f"{slug}.pdf"
                dst_pdf.write_bytes(src_pdf.read_bytes())
                print(f"  📄 Copied {pdf_name} -> {slug}.pdf")
                pdf_found = True
                break
        
        if not pdf_found:
            print(f"  ⚠️  No PDF found for {slug} - will skip PDF link")
