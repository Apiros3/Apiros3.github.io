#!/usr/bin/env python3
import json, os, re, datetime
from pathlib import Path
import sys
sys.path.append('script')
from generate_publications import get_publications

POSTS_SRC = Path("posts")
BUILD     = Path("build")
POSTS_OUT = BUILD / "posts"
PDF_OUT   = BUILD / "pdf"

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
    posts = []
    for tex in POSTS_SRC.glob("*.tex"):
        date_str, slug = parse_name(tex)
        meta = read_meta(slug)
        title = meta.get("title") or slug.replace("-", " ").title()
        tags  = meta.get("tags", [])
        html_path = POSTS_OUT / slug / "index.html"
        if html_path.exists():
            posts.append({
                "date": date_str, "slug": slug,
                "title": title, "tags": tags,
                "date_obj": datetime.datetime.strptime(date_str, "%Y-%m-%d")
            })
    
    # Sort by date (newest first)
    posts.sort(key=lambda p: p["date_obj"], reverse=True)
    return posts

def build_academic_homepage(posts):
    # Get recent articles (first 5)
    recent_articles = posts[:5]
    
    # Build articles HTML
    articles_html = ""
    for p in recent_articles:
        tags = ", ".join(p.get("tags", [])) if p.get("tags") else ""
        articles_html += f'''
      <li class="post-item">
        <a href="posts/{p["slug"]}/index.html" class="post-title">{p["title"]}</a>
        <div class="post-meta">
          <span class="post-date">{p["date"]}</span>
          {f'<span class="post-tags"> • {tags}</span>' if tags else ''}
        </div>
        <a href="pdf/{p["slug"]}.pdf" class="post-download" target="_blank">📄 PDF</a>
      </li>'''
    
    # Get publications
    publications = get_publications()
    publications_html = ""
    if publications:
        publications_html = '''
    <section class="publications-section">
      <h2>Recent Publications</h2>
      <ul class="publication-list">'''
        for pub in publications[:5]:  # Show first 5 publications
            publications_html += f'''
        <li class="publication-item">
          <div class="publication-info">
            <h3 class="publication-title">{pub["title"]}</h3>
            <span class="publication-year">({pub["year"]})</span>
          </div>
          <a href="{pub["path"]}" class="publication-download" target="_blank">📄 PDF</a>
        </li>'''
        publications_html += '''
      </ul>
    </section>'''
    
    # Build navigation menu
    nav_items = []
    for p in posts[:10]:  # Show first 10 posts in nav
        nav_items.append(f'<a href="posts/{p["slug"]}/index.html">{p["title"]}</a>')
    nav_menu = '\n        '.join(nav_items)
    
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Apiros3 - Academic Homepage</title>
  <link rel="stylesheet" href="assets/main.css">
  <style>
    .hero {{
      background: linear-gradient(135deg, #007cba 0%, #005a87 100%);
      color: white;
      padding: 4em 0;
      text-align: center;
      margin-bottom: 3em;
    }}
    .hero h1 {{
      font-size: 3em;
      margin: 0 0 0.5em 0;
      font-weight: 300;
    }}
    .hero p {{
      font-size: 1.2em;
      margin: 0;
      opacity: 0.9;
    }}
    .content-section {{
      margin: 3em 0;
      padding: 2em 0;
    }}
    .content-section h2 {{
      color: #333;
      border-bottom: 2px solid #007cba;
      padding-bottom: 0.5em;
      margin-bottom: 1.5em;
      font-size: 1.8em;
    }}
    .post-list {{
      list-style: none;
      padding: 0;
    }}
    .post-item {{
      margin: 1.5em 0;
      padding: 1.5em;
      border: 1px solid #eee;
      border-radius: 8px;
      background: #fafafa;
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: box-shadow 0.2s;
    }}
    .post-item:hover {{
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    .post-title {{
      text-decoration: none;
      color: #333;
      font-size: 1.2em;
      font-weight: bold;
      flex: 1;
    }}
    .post-title:hover {{
      color: #007cba;
    }}
    .post-meta {{
      color: #666;
      font-size: 0.9em;
      margin: 0.5em 0;
    }}
    .post-download {{
      background: #007cba;
      color: white;
      padding: 0.5em 1em;
      border-radius: 4px;
      text-decoration: none;
      font-size: 0.9em;
      margin-left: 1em;
    }}
    .post-download:hover {{
      background: #005a87;
    }}
    .publication-list {{
      list-style: none;
      padding: 0;
    }}
    .publication-item {{
      margin: 1.5em 0;
      padding: 1.5em;
      border: 1px solid #ddd;
      border-radius: 8px;
      background: #f9f9f9;
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: box-shadow 0.2s;
    }}
    .publication-item:hover {{
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    .publication-info {{
      flex: 1;
    }}
    .publication-title {{
      margin: 0 0 0.5em 0;
      font-size: 1.1em;
      color: #333;
    }}
    .publication-year {{
      color: #666;
      font-size: 0.9em;
    }}
    .publication-download {{
      background: #28a745;
      color: white;
      padding: 0.5em 1em;
      border-radius: 4px;
      text-decoration: none;
      font-size: 0.9em;
      margin-left: 1em;
    }}
    .publication-download:hover {{
      background: #218838;
    }}
    .site-header {{
      background: #007cba;
      color: white;
      padding: 1em 0;
      margin-bottom: 0;
    }}
    .brand {{
      color: white;
      text-decoration: none;
      font-size: 1.5em;
      font-weight: bold;
    }}
    .nav-menu {{
      background: #005a87;
      padding: 0.5em 0;
      margin-top: 1em;
    }}
    .nav-menu a {{
      color: white;
      text-decoration: none;
      padding: 0.3em 0.8em;
      margin: 0.2em 0;
      border-radius: 3px;
      font-size: 0.9em;
      transition: background 0.2s;
      display: block;
    }}
    .nav-menu a:hover {{
      background: rgba(255,255,255,0.2);
    }}
    .nav-toggle {{
      display: none;
      background: none;
      border: none;
      color: white;
      font-size: 1.2em;
      cursor: pointer;
    }}
    .contact-section {{
      background: #f8f9fa;
      padding: 2em;
      border-radius: 8px;
      margin: 2em 0;
    }}
    .contact-section h3 {{
      margin-top: 0;
      color: #333;
    }}
    .contact-info {{
      color: #666;
      line-height: 1.6;
    }}
    @media (max-width: 768px) {{
      .nav-menu {{
        display: none;
      }}
      .nav-menu.show {{
        display: block;
      }}
      .nav-toggle {{
        display: block;
      }}
      .hero h1 {{
        font-size: 2em;
      }}
      .post-item {{
        flex-direction: column;
        align-items: flex-start;
      }}
      .post-download, .publication-download {{
        margin-left: 0;
        margin-top: 1em;
      }}
    }}
  </style>
</head>
<body>
  <header class="site-header">
    <div class="container">
      <a class="brand" href="./index.html">📚 Apiros3</a>
      <button class="nav-toggle" onclick="toggleNav()">☰</button>
    </div>
    <nav class="nav-menu" id="navMenu">
      <div class="container">
        {nav_menu}
      </div>
    </nav>
  </header>
  <script>
    function toggleNav() {{
      const nav = document.getElementById('navMenu');
      nav.classList.toggle('show');
    }}
  </script>

  <div class="hero">
    <div class="container">
      <h1>Apiros3</h1>
      <p>Research Scientist | Mathematics & Computer Science</p>
    </div>
  </div>

  <main class="container">
    <section class="content-section">
      <h2>About</h2>
      <p>Welcome to my academic homepage. I am a research scientist working on mathematics and computer science. My research interests include algebraic structures, formal methods, and theoretical computer science. I am particularly passionate about the intersection of algebra and logic in computational systems.</p>
    </section>

    <section class="content-section">
      <h2>Recent Articles</h2>
      <ul class="post-list">
        {articles_html}
      </ul>
    </section>
{publications_html}
    <section class="content-section">
      <div class="contact-section">
        <h3>Contact</h3>
        <div class="contact-info">
          <p><strong>Email:</strong> your.email@institution.edu</p>
          <p><strong>Research Interests:</strong> Algebra, Logic, Formal Methods, Type Theory</p>
          <p><strong>Location:</strong> [Your Institution]</p>
        </div>
      </div>
    </section>
  </main>
</body>
</html>"""

def main():
    posts = get_all_posts()
    homepage_html = build_academic_homepage(posts)
    print("Generated academic homepage HTML (not saved to file)")

if __name__ == "__main__":
    main()

