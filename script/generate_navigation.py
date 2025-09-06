#!/usr/bin/env python3
import json, os, re, datetime
from pathlib import Path

POSTS_SRC = Path("posts")
BUILD = Path("build")
POSTS_OUT = BUILD / "posts"

def parse_name(tex_path: Path):
    """
    Expect filenames like YYYY-MM-DD-slug.tex
    Returns (date_str, slug)
    """
    base = tex_path.stem
    m = re.match(r"(\d{4}-\d{2}-\d{2})-(.+)", base)
    if m:
        return m.group(1), m.group(2)
    # fallback: today's date and basename
    return datetime.date.today().isoformat(), base

def read_meta(slug: str):
    meta_path = POSTS_SRC / f"{slug}.meta.json"
    if meta_path.exists():
        with open(meta_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def get_all_posts():
    """Get all posts sorted by date"""
    posts = []
    for tex in POSTS_SRC.glob("*.tex"):
        date_str, slug = parse_name(tex)
        meta = read_meta(slug)
        title = meta.get("title") or slug.replace("-", " ").title()
        html_path = POSTS_OUT / slug / "index.html"
        if html_path.exists():
            posts.append({
                "date": date_str, "slug": slug,
                "title": title, "date_obj": datetime.datetime.strptime(date_str, "%Y-%m-%d")
            })
    
    # Sort by title alphabetically
    posts.sort(key=lambda p: p["title"].lower())
    return posts

def add_navigation_to_post(post_slug, all_posts):
    """Add navigation to a specific post"""
    post_path = POSTS_OUT / post_slug / "index.html"
    if not post_path.exists():
        return
    
    # Find current post index
    current_index = None
    for i, post in enumerate(all_posts):
        if post["slug"] == post_slug:
            current_index = i
            break
    
    if current_index is None:
        return
    
    # Generate header navigation menu
    nav_items = []
    for p in all_posts[:10]:  # Show first 10 posts in nav
        nav_items.append(f'<a href="../{p["slug"]}/index.html">{p["title"]}</a>')
    nav_menu = '\n        '.join(nav_items)
    
    # No bottom navigation needed - only header navigation
    
    # Read current HTML
    with open(post_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add navigation menu to header
    content = content.replace('<!-- Navigation will be added by script -->', nav_menu)
    
    # Write back
    with open(post_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    all_posts = get_all_posts()
    
    # Add navigation to each post
    for post in all_posts:
        add_navigation_to_post(post["slug"], all_posts)
    
    print(f"Added navigation to {len(all_posts)} posts")

if __name__ == "__main__":
    main()
