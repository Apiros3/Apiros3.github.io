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

from script.data_loader import get_all_posts, get_publications, get_talks, get_notes, get_reading_list, copy_blog_posts, copy_pdf_files
from script.page_generators import generate_main_index, generate_blog_listing, generate_publications_page, generate_notes_page, generate_reading_list_page


def main():
    """Main generation function."""
    print("🚀 Generating academic portfolio...")
    print("📄 Loading site configuration from site.meta.json...")
    
    # Files are generated in place
    
    # Get data
    posts = get_all_posts()
    publications = get_publications()
    talks = get_talks()
    notes = get_notes()
    reading_list = get_reading_list()
    
    print(f"Found {len(posts)} blog posts")
    print(f"Found {len(publications)} publications")
    print(f"Found {len(talks)} talks")
    print(f"Found {len(notes)} notes")
    print(f"Found {len(reading_list)} reading list items")
    
    # Generate pages
    print("Generating main index...")
    main_html = generate_main_index(posts)
    Path("index.html").write_text(main_html, encoding="utf-8")
    
    print("Generating blog listing...")
    blog_html = generate_blog_listing(posts)
    # Write blog listing to posts directory (already exists from blog build)
    Path("posts/index.html").write_text(blog_html, encoding="utf-8")
    
    print("Generating publications page...")
    pub_html = generate_publications_page(publications, talks)
    # Create publications directory if it doesn't exist
    publications_dir = Path("publications")
    publications_dir.mkdir(exist_ok=True)
    (publications_dir / "index.html").write_text(pub_html, encoding="utf-8")
    
    print("Generating notes page...")
    notes_html = generate_notes_page(notes)
    # Create notes-page directory if it doesn't exist
    notes_dir = Path("notes-page")
    notes_dir.mkdir(exist_ok=True)
    (notes_dir / "index.html").write_text(notes_html, encoding="utf-8")
    
    print("Generating reading list page...")
    reading_list_html = generate_reading_list_page(reading_list)
    # Create reading-list directory if it doesn't exist
    reading_list_dir = Path("reading-list")
    reading_list_dir.mkdir(exist_ok=True)
    (reading_list_dir / "index.html").write_text(reading_list_html, encoding="utf-8")
    
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
    print(f"  📄 notes-page/index.html (notes)")
    print(f"  📄 reading-list/index.html (reading list)")
    print(f"  📁 posts/ (blog post HTML files)")
    print(f"  📁 Notes/publication/ (PDF files)")


if __name__ == "__main__":
    main()
