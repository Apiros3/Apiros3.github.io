#!/usr/bin/env python3
"""
Unified site generation script for academic portfolio.
Generates all HTML pages from metadata and TeX sources.
"""
from pathlib import Path
import sys
import os

# Add the script directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from script.config import BUILD
from script.data_loader import get_all_posts, get_publications, copy_blog_posts, copy_pdf_files
from script.page_generators import generate_main_index, generate_blog_listing, generate_publications_page


def main():
    """Main generation function."""
    print("🚀 Generating academic portfolio...")
    
    # Create build directory
    BUILD.mkdir(exist_ok=True)
    
    # Get data
    posts = get_all_posts()
    publications = get_publications()
    
    print(f"Found {len(posts)} blog posts")
    print(f"Found {len(publications)} publications")
    
    # Generate pages
    print("Generating main index...")
    main_html = generate_main_index(posts)
    Path("index.html").write_text(main_html, encoding="utf-8")
    
    print("Generating blog listing...")
    blog_html = generate_blog_listing(posts)
    # Create posts directory if it doesn't exist
    posts_dir = Path("posts")
    posts_dir.mkdir(exist_ok=True)
    (posts_dir / "index.html").write_text(blog_html, encoding="utf-8")
    
    print("Generating publications page...")
    pub_html = generate_publications_page(publications)
    # Create publications directory if it doesn't exist
    publications_dir = Path("publications")
    publications_dir.mkdir(exist_ok=True)
    (publications_dir / "index.html").write_text(pub_html, encoding="utf-8")
    
    # Copy blog post files
    print("Copying blog post files...")
    copy_blog_posts(posts)
    
    # Copy PDF files
    print("Copying PDF files...")
    copy_pdf_files(posts)
    
    print("✅ Site generation completed!")
    print(f"Generated files:")
    print(f"  📄 index.html (main page)")
    print(f"  📄 posts/index.html (blog listing)")
    print(f"  📄 publications/index.html (publications)")
    print(f"  📁 posts/ (blog post HTML files)")
    print(f"  📁 Notes/publication/ (PDF files)")


if __name__ == "__main__":
    main()
