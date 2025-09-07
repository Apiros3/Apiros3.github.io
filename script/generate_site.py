#!/usr/bin/env python3
"""
Unified site generation script for academic portfolio.
Generates all HTML pages from metadata and TeX sources.
"""
import json
import re
import datetime
from pathlib import Path

# Configuration
POSTS_SRC = Path("posts")
BUILD = Path("build")
PDF_OUT = BUILD / "pdf"

def parse_tex_filename(tex_path: Path):
    """Parse YYYY-MM-DD-slug.tex filename format."""
    base = tex_path.stem
    match = re.match(r"(\d{4}-\d{2}-\d{2})-(.+)", base)
    if match:
        return match.group(1), match.group(2)
    return datetime.date.today().isoformat(), base

def read_metadata(slug: str):
    """Read metadata from .meta.json file."""
    meta_path = POSTS_SRC / f"{slug}.meta.json"
    if meta_path.exists():
        with open(meta_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def get_all_posts():
    """Get all blog posts with metadata."""
    posts = []
    for tex_file in POSTS_SRC.glob("*.tex"):
        date_str, slug = parse_tex_filename(tex_file)
        meta = read_metadata(slug)
        
        # Only include if HTML output exists
        html_path = POSTS_SRC / slug / "index.html"
        if html_path.exists():
            # Check if PDF exists in the post directory
            has_pdf = False
            pdf_path = POSTS_SRC / slug / f"{slug}.pdf"
            if pdf_path.exists():
                has_pdf = True
            
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

def get_publications():
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

def generate_common_css():
    """Generate common CSS styles."""
    return """
    .hero {
      background: linear-gradient(135deg, #007cba 0%, #005a87 100%);
      color: white;
      padding: 2em 0;
      text-align: center;
      margin-bottom: 2em;
    }
    .hero h1 {
      font-size: 2.5em;
      margin: 0 0 0.5em 0;
      font-weight: 300;
    }
    .hero p {
      font-size: 1.1em;
      margin: 0;
      opacity: 0.9;
    }
    .site-header {
      background: #fff;
      border-bottom: 1px solid #e9ecef;
      padding: 1rem 0;
      margin-bottom: 0;
      position: sticky;
      top: 0;
      z-index: 1000;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .site-header .container {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .brand {
      color: #333;
      text-decoration: none;
      font-size: 1.5em;
      font-weight: 700;
      letter-spacing: -0.5px;
    }
    .brand:hover {
      color: #007cba;
    }
    .main-nav {
      display: flex;
      align-items: center;
    }
    .nav-list {
      display: flex;
      list-style: none;
      margin: 0;
      padding: 0;
      gap: 2rem;
    }
    .nav-item {
      margin: 0;
    }
    .nav-link {
      color: #333;
      text-decoration: none;
      font-weight: 500;
      font-size: 0.95em;
      padding: 0.5rem 0;
      transition: color 0.2s ease;
      position: relative;
    }
    .nav-link:hover, .nav-link.current {
      color: #007cba;
    }
    .nav-link::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      width: 0;
      height: 2px;
      background: #007cba;
      transition: width 0.3s ease;
    }
    .nav-link:hover::after, .nav-link.current::after {
      width: 100%;
    }
    .nav-toggle {
      display: none;
      background: none;
      border: none;
      font-size: 1.2em;
      cursor: pointer;
      color: #333;
      padding: 0.5rem;
    }
    @media (max-width: 768px) {
      .nav-toggle {
        display: block;
      }
      .main-nav {
        display: none;
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: #fff;
        border-top: 1px solid #e9ecef;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
      }
      .main-nav.show {
        display: block;
      }
      .nav-list {
        flex-direction: column;
        gap: 0;
        padding: 1rem 0;
      }
      .nav-item {
        border-bottom: 1px solid #f0f0f0;
      }
      .nav-item:last-child {
        border-bottom: none;
      }
      .nav-link {
        display: block;
        padding: 1rem 2rem;
        color: #333;
      }
      .nav-link::after {
        display: none;
      }
    }
    """

def generate_main_index(posts):
    """Generate the main index page."""
    # Generate recent posts (first 5)
    recent_items = []
    for post in posts[:5]:
        pdf_link = f'<a href="posts/{post["slug"]}/{post["slug"]}.pdf" class="post-download" target="_blank">PDF</a>' if post.get("has_pdf", False) else ''
        recent_items.append(f'''
        <li class="post-item">
          <a href="posts/{post["slug"]}/index.html" class="post-title">{post["title"]}</a>
          <span class="post-date">{post["date"]}</span>
          {pdf_link}
        </li>''')
    
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Apiros3 - Academic Portfolio</title>
  <link rel="stylesheet" href="asset/main.css">
  <style>
    {generate_common_css()}
    .main-layout {{
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: 3rem;
      margin: 2rem 0;
    }}
    .content-section {{
      margin-bottom: 3rem;
    }}
    .content-section h2 {{
      color: #333;
      border-bottom: 2px solid #007cba;
      padding-bottom: 0.5rem;
      margin-bottom: 1.5rem;
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
    .post-date {{
      color: #666;
      font-size: 0.9em;
      margin: 0 1em;
    }}
    .post-download {{
      background: #007cba;
      color: white;
      padding: 0.5em 1em;
      border-radius: 4px;
      text-decoration: none;
      font-size: 0.9em;
    }}
    .post-download:hover {{
      background: #005a87;
    }}
    .sidebar {{
      background: #f8f9fa;
      padding: 2rem;
      border-radius: 8px;
      height: fit-content;
      position: sticky;
      top: 2rem;
    }}
    .sidebar h3 {{
      color: #333;
      margin-bottom: 1rem;
    }}
    .contact-info-sidebar p {{
      margin: 1rem 0;
      line-height: 1.5;
    }}
    @media (max-width: 768px) {{
      .main-layout {{
        grid-template-columns: 1fr;
        gap: 2rem;
      }}
      .post-item {{
        flex-direction: column;
        align-items: flex-start;
      }}
      .post-download {{
        margin-left: 0;
        margin-top: 1em;
      }}
    }}
  </style>
  <script>
    function toggleNav() {{
      const nav = document.querySelector('.main-nav');
      nav.classList.toggle('show');
    }}
  </script>
</head>
<body>
  <header class="site-header">
    <div class="container">
      <a class="brand" href="./index.html">Apiros3</a>
      <nav class="main-nav">
        <ul class="nav-list">
          <li class="nav-item"><a href="./index.html" class="nav-link current">About</a></li>
          <li class="nav-item"><a href="build/publications.html" class="nav-link">Publications</a></li>
          <li class="nav-item"><a href="posts/index.html" class="nav-link">Blog</a></li>
        </ul>
      </nav>
      <button class="nav-toggle" onclick="toggleNav()">☰</button>
    </div>
  </header>

  <div class="hero">
    <div class="container">
      <h1>Apiros3</h1>
      <p>Research Scientist, Mathematics & Computer Science</p>
    </div>
  </div>

  <main class="container">
    <div class="main-layout">
      <div class="main-content">
        <section class="content-section" id="about">
          <h2>About</h2>
          <p>Welcome to my academic portfolio. I am a research scientist working at the intersection of mathematics and computer science. My research focuses on algebraic structures, formal methods, and theoretical computer science, with particular emphasis on the connections between algebra and logic in computational systems.</p>
        </section>

        <section class="content-section" id="articles">
          <h2>Recent Blog Posts</h2>
          <div class="articles-container">
            <ul class="post-list">
              {''.join(recent_items)}
            </ul>
            <div class="load-more-container">
              <a href="posts/index.html" class="load-more-btn">View All Articles</a>
            </div>
          </div>
        </section>
      </div>
      
      <div class="sidebar">
        <h3>Contact</h3>
        <div class="contact-info-sidebar">
          <p><strong>Email:</strong><br>your.email@institution.edu</p>
          <p><strong>Institution:</strong><br>[Your Institution]</p>
          <p><strong>Department:</strong><br>Mathematics & Computer Science</p>
          <p><strong>Location:</strong><br>[Your Location]</p>
        </div>
      </div>
    </div>
  </main>
</body>
</html>"""

def generate_blog_listing(posts):
    """Generate the blog listing page."""
    # Generate all posts
    all_items = []
    for post in posts:
        tags_html = ""
        if post["tags"]:
            tags_html = f"""
            <div class="post-tags">
              {''.join(f'<span class="post-tag">#{tag}</span>' for tag in post["tags"])}
            </div>"""
        
        abstract_html = ""
        if post.get("abstract"):
            abstract_html = f'<div class="post-abstract">{post["abstract"]}</div>'
        
        pdf_link = f'<a href="posts/{post["slug"]}/{post["slug"]}.pdf" class="post-download" target="_blank">PDF</a>' if post.get("has_pdf", False) else ''
        all_items.append(f"""
        <li class="post-item" data-tags="{','.join(post["tags"])}">
          <div class="post-header">
            <a href="posts/{post["slug"]}/index.html" class="post-title">{post["title"]}</a>
            {pdf_link}
          </div>
          <div class="post-meta">
            <span class="post-date">{post["date"]}</span>
            {tags_html}
          </div>
          {abstract_html}
        </li>""")
    
    # Get all unique tags
    all_tags = set()
    for post in posts:
        all_tags.update(post["tags"])
    all_tags = sorted(list(all_tags))
    
    # Generate tag filter buttons
    tag_buttons = ['<button class="tag-filter active" data-tag="all">All</button>']
    for tag in all_tags:
        tag_buttons.append(f'<button class="tag-filter" data-tag="{tag}">{tag.title()}</button>')
    
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Blog - Apiros3</title>
  <link rel="stylesheet" href="../asset/main.css">
  <style>
    {generate_common_css()}
    .back-link {{
      display: inline-block;
      margin-bottom: 1em;
      color: #007cba;
      text-decoration: none;
      font-weight: 500;
    }}
    .back-link:hover {{
      text-decoration: underline;
    }}
    .filter-section {{
      margin: 2em 0;
      padding: 1.5em;
      background: #f8f9fa;
      border-radius: 8px;
    }}
    .filter-section h3 {{
      margin: 0 0 1em 0;
      color: #333;
    }}
    .tag-filters {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5em;
    }}
    .tag-filter {{
      padding: 0.5em 1em;
      border: 1px solid #ddd;
      background: white;
      color: #666;
      border-radius: 20px;
      cursor: pointer;
      transition: all 0.2s ease;
      font-size: 0.9em;
    }}
    .tag-filter:hover {{
      background: #e9ecef;
      color: #333;
    }}
    .tag-filter.active {{
      background: #007cba;
      color: white;
      border-color: #007cba;
    }}
    .post-list {{
      list-style: none;
      padding: 0;
    }}
    .post-item {{
      margin: 2em 0;
      padding: 2em;
      border: 1px solid #eee;
      border-radius: 8px;
      background: #fafafa;
      display: flex;
      flex-direction: column;
      transition: box-shadow 0.2s;
    }}
    .post-item:hover {{
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}
    .post-item.hidden {{
      display: none;
    }}
    .post-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 1em;
    }}
    .post-title {{
      font-size: 1.3em;
      font-weight: bold;
      color: #333;
      margin: 0;
      flex: 1;
      line-height: 1.3;
      text-decoration: none;
    }}
    .post-title:hover {{
      color: #007cba;
    }}
    .post-download {{
      background: #007cba;
      color: white;
      padding: 0.4em 0.8em;
      border-radius: 4px;
      text-decoration: none;
      font-size: 0.85em;
      font-weight: 500;
      white-space: nowrap;
      margin-left: 1em;
    }}
    .post-download:hover {{
      background: #005a87;
    }}
    .post-meta {{
      margin-bottom: 1em;
    }}
    .post-date {{
      color: #666;
      font-size: 0.95em;
    }}
    .post-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.3em;
      margin-top: 0.5em;
    }}
    .post-tag {{
      background: #f8f9fa;
      color: #666;
      padding: 0.2em 0.6em;
      border-radius: 12px;
      font-size: 0.75em;
      font-weight: 400;
      border: 1px solid #e9ecef;
      transition: all 0.2s ease;
      display: inline-block;
      margin: 0.1em;
      text-transform: lowercase;
      letter-spacing: 0.3px;
    }}
    .post-tag:hover {{
      background: #e9ecef;
      color: #495057;
    }}
    .post-abstract {{
      color: #555;
      font-size: 1em;
      line-height: 1.6;
      font-style: italic;
      background: #f8f9fa;
      padding: 1em;
      border-left: 4px solid #007cba;
      border-radius: 0 4px 4px 0;
    }}
    @media (max-width: 768px) {{
      .post-header {{
        flex-direction: column;
        align-items: flex-start;
      }}
      .post-download {{
        margin-left: 0;
        margin-top: 0.5em;
      }}
    }}
  </style>
  <script>
    function toggleNav() {{
      const nav = document.querySelector('.main-nav');
      nav.classList.toggle('show');
    }}
    
    // Tag filtering functionality
    document.addEventListener('DOMContentLoaded', function() {{
      const filterButtons = document.querySelectorAll('.tag-filter');
      const postItems = document.querySelectorAll('.post-item');
      
      filterButtons.forEach(button => {{
        button.addEventListener('click', function() {{
          const selectedTag = this.getAttribute('data-tag');
          
          // Update active button
          filterButtons.forEach(btn => btn.classList.remove('active'));
          this.classList.add('active');
          
          // Filter posts
          postItems.forEach(item => {{
            const itemTags = item.getAttribute('data-tags');
            if (selectedTag === 'all' || (itemTags && itemTags.includes(selectedTag))) {{
              item.classList.remove('hidden');
            }} else {{
              item.classList.add('hidden');
            }}
          }});
        }});
      }});
    }});
  </script>
</head>
<body>
  <header class="site-header">
    <div class="container">
      <a class="brand" href="../index.html">Apiros3</a>
      <nav class="main-nav">
        <ul class="nav-list">
          <li class="nav-item"><a href="../index.html" class="nav-link">About</a></li>
          <li class="nav-item"><a href="publications.html" class="nav-link">Publications</a></li>
          <li class="nav-item"><a href="index.html" class="nav-link current">Blog</a></li>
        </ul>
      </nav>
      <button class="nav-toggle" onclick="toggleNav()">☰</button>
    </div>
  </header>

  <div class="hero">
    <div class="container">
      <h1>Blog</h1>
      <p>Complete list of blog posts and research notes</p>
    </div>
  </div>

  <main class="container">
    <a href="../index.html" class="back-link">← Back to Mainpage</a>
    
    <div class="filter-section">
      <h3>Filter by Tag</h3>
      <div class="tag-filters">
        {''.join(tag_buttons)}
      </div>
    </div>
    
    <ul class="post-list">
      {''.join(all_items)}
    </ul>
  </main>
</body>
</html>"""

def generate_publications_page(publications):
    """Generate the publications page."""
    # Generate publication items
    pub_items = []
    pub_dir = Path("publications/data")
    
    for i, pub in enumerate(publications):
        title = pub.get("title", "Untitled")
        authors = pub.get("authors", [])
        conference = pub.get("conference", "Unknown")
        year = pub.get("year", "Unknown")
        abstract = pub.get("abstract", "")
        arxiv = pub.get("arxiv", "")
        doi = pub.get("doi", "")
        code = pub.get("code", "")
        venue = pub.get("venue", "")
        pages = pub.get("pages", "")
        
        # Format authors
        if isinstance(authors, list):
            authors_str = ", ".join(authors)
        else:
            authors_str = str(authors)
        
        # Format venue info
        venue_info = f"{conference}"
        if venue:
            venue_info += f" ({venue})"
        if year:
            venue_info += f", {year}"
        
        # Generate links
        links_html = ""
        if arxiv:
            links_html += f'<a href="{arxiv}" class="pub-link arxiv-link" target="_blank">arXiv</a>'
        if doi:
            links_html += f'<a href="{doi}" class="pub-link doi-link" target="_blank">DOI</a>'
        if code:
            links_html += f'<a href="{code}" class="pub-link code-link" target="_blank">Code</a>'
        
        # Check if PDF exists - try different naming patterns
        meta_files = list(pub_dir.glob("*.meta.json"))
        meta_file = meta_files[i] if i < len(meta_files) else None
        
        possible_pdf_names = [
            f"{pub.get('filename', 'itp25')}.pdf",  # from filename field
            f"{meta_file.stem.replace('.meta', '')}.pdf" if meta_file else "itp25.pdf",  # from metadata filename
            f"{title.lower().replace(' ', '-')}.pdf",  # from title
            "2025-09-06-template.pdf",  # actual PDF that exists
            "itp25.pdf"  # fallback
        ]
        
        pdf_found = False
        # First check posts directory (where the actual PDF is)
        for pdf_name in possible_pdf_names:
            pdf_path = Path("posts") / pdf_name
            if pdf_path.exists():
                links_html += f'<a href="../posts/{pdf_name}" class="pub-link pdf-link" target="_blank">PDF</a>'
                pdf_found = True
                break
        
        # If no PDF found in posts, check Notes/publication directory
        if not pdf_found:
            for pdf_name in possible_pdf_names:
                pdf_path = Path("Notes/publication") / pdf_name
                if pdf_path.exists():
                    links_html += f'<a href="../Notes/publication/{pdf_name}" class="pub-link pdf-link" target="_blank">PDF</a>'
                    pdf_found = True
                    break
        
        pub_items.append(f"""
        <li class="publication-item">
          <div class="publication-header">
            <h3 class="publication-title">{title}</h3>
            <div class="publication-links">
              {links_html}
            </div>
          </div>
          <div class="publication-meta">
            <div class="publication-authors">{authors_str}</div>
            <div class="publication-venue">{venue_info}</div>
            {f'<div class="publication-pages">{pages}</div>' if pages else ''}
          </div>
          {f'<div class="publication-abstract">{abstract}</div>' if abstract else ''}
        </li>""")
    
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Publications - Apiros3</title>
  <link rel="stylesheet" href="../asset/main.css">
  <style>
    {generate_common_css()}
    .back-link {{
      display: inline-block;
      margin-bottom: 1em;
      color: #007cba;
      text-decoration: none;
      font-weight: 500;
    }}
    .back-link:hover {{
      text-decoration: underline;
    }}
    .publication-list {{
      list-style: none;
      padding: 0;
    }}
    .publication-item {{
      margin: 2em 0;
      padding: 2em;
      border: 1px solid #eee;
      border-radius: 8px;
      background: #fafafa;
      display: flex;
      flex-direction: column;
      transition: box-shadow 0.2s;
    }}
    .publication-item:hover {{
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}
    .publication-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 1em;
    }}
    .publication-title {{
      font-size: 1.3em;
      font-weight: bold;
      color: #333;
      margin: 0;
      flex: 1;
      line-height: 1.3;
    }}
    .publication-links {{
      display: flex;
      gap: 0.5em;
      margin-left: 1em;
    }}
    .pub-link {{
      padding: 0.4em 0.8em;
      border-radius: 4px;
      text-decoration: none;
      font-size: 0.85em;
      font-weight: 500;
      white-space: nowrap;
    }}
    .arxiv-link {{
      background: #ff6b35;
      color: white;
    }}
    .arxiv-link:hover {{
      background: #e55a2b;
    }}
    .doi-link {{
      background: #007cba;
      color: white;
    }}
    .doi-link:hover {{
      background: #005a87;
    }}
    .pdf-link {{
      background: #28a745;
      color: white;
    }}
    .pdf-link:hover {{
      background: #218838;
    }}
    .code-link {{
      background: #6f42c1;
      color: white;
    }}
    .code-link:hover {{
      background: #5a32a3;
    }}
    .publication-meta {{
      margin-bottom: 1em;
    }}
    .publication-authors {{
      color: #555;
      font-size: 1em;
      margin-bottom: 0.3em;
      font-weight: 500;
    }}
    .publication-venue {{
      color: #666;
      font-size: 0.95em;
      font-style: italic;
    }}
    .publication-pages {{
      color: #666;
      font-size: 0.9em;
      margin-top: 0.2em;
    }}
    .publication-abstract {{
      color: #555;
      font-size: 1em;
      line-height: 1.6;
      font-style: italic;
      background: #f8f9fa;
      padding: 1em;
      border-left: 4px solid #007cba;
      border-radius: 0 4px 4px 0;
    }}
    @media (max-width: 768px) {{
      .publication-header {{
        flex-direction: column;
        align-items: flex-start;
      }}
      .publication-links {{
        margin-left: 0;
        margin-top: 0.5em;
      }}
    }}
  </style>
  <script>
    function toggleNav() {{
      const nav = document.querySelector('.main-nav');
      nav.classList.toggle('show');
    }}
  </script>
</head>
<body>
  <header class="site-header">
    <div class="container">
      <a class="brand" href="../index.html">Apiros3</a>
      <nav class="main-nav">
        <ul class="nav-list">
          <li class="nav-item"><a href="../index.html" class="nav-link">About</a></li>
          <li class="nav-item"><a href="publications.html" class="nav-link current">Publications</a></li>
          <li class="nav-item"><a href="index.html" class="nav-link">Blog</a></li>
        </ul>
      </nav>
      <button class="nav-toggle" onclick="toggleNav()">☰</button>
    </div>
  </header>

  <div class="hero">
    <div class="container">
      <h1>Publications</h1>
      <p>Research papers and academic publications</p>
    </div>
  </div>

  <main class="container">
    <a href="../index.html" class="back-link">← Back to Mainpage</a>
    
    <ul class="publication-list">
      {''.join(pub_items)}
    </ul>
  </main>
</body>
</html>"""

# Blog posts are now used directly from posts/ directory
# No copying needed

# PDF files are now used directly from posts/ directory
# No copying needed

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
    (BUILD / "index.html").write_text(blog_html, encoding="utf-8")
    
    print("Generating publications page...")
    pub_html = generate_publications_page(publications)
    (BUILD / "publications.html").write_text(pub_html, encoding="utf-8")
    
    # Blog posts and PDFs are used directly from posts/ directory
    print("Using blog posts and PDFs directly from posts/ directory...")
    
    print("✅ Site generation completed!")
    print(f"Generated files:")
    print(f"  📄 index.html (main page)")
    print(f"  📄 build/index.html (blog listing)")
    print(f"  📄 build/publications.html (publications)")
    print(f"  📁 posts/ (blog posts and PDFs - used directly)")

if __name__ == "__main__":
    main()