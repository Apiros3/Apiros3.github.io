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

def build_index(posts):
    posts.sort(key=lambda p: p["date"], reverse=True)
    # Build recent articles section
    recent_items = []
    for p in posts[:5]:  # Show only 5 most recent articles
        recent_items.append(f'''
      <li class="post-item">
        <a href="posts/{p["slug"]}/index.html" class="post-title">{p["title"]}</a>
        <span class="post-date">{p["date"]}</span>
        <a href="pdf/{p["slug"]}.pdf" class="post-download" target="_blank">PDF</a>
      </li>''')
    
    # Build all articles section
    all_items = []
    for p in posts:
        tags = ", ".join(p.get("tags", [])) if p.get("tags") else ""
        all_items.append(f'''
      <li class="post-item">
        <a href="posts/{p["slug"]}/index.html" class="post-title">{p["title"]}</a>
        <div class="post-meta">
          <span class="post-date">{p["date"]}</span>
          {f'<span class="post-tags"> • {tags}</span>' if tags else ''}
        </div>
        <a href="pdf/{p["slug"]}.pdf" class="post-download" target="_blank">PDF</a>
      </li>''')
    
    # Build publications section
    publications = get_publications()
    publications_html = ""
    if publications:
        publications_html = f'''
    <section class="publications-section">
      <h2>Recent Publications</h2>
      <ul class="publication-list">
'''
        for pub in publications[:5]:  # Show only 5 most recent publications
            publications_html += f'''        <li class="publication-item">
          <div class="publication-info">
            <h3 class="publication-title">{pub["title"]}</h3>
            <span class="publication-year">({pub["year"]})</span>
          </div>
          <a href="{pub["path"]}" class="publication-download" target="_blank">PDF</a>
        </li>
'''
        publications_html += '''      </ul>
    </section>
'''
    
    # Build navigation menu
    nav_items = []
    for p in posts[:8]:  # Show first 8 posts in nav
        nav_items.append(f'<a href="posts/{p["slug"]}/index.html">{p["title"]}</a>')
    nav_menu = '\n        '.join(nav_items)
    
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Apiros3 - Academic Portfolio</title>
  <link rel="stylesheet" href="asset/main.css">
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
    .research-interests {{
      background: #f0f8ff;
      padding: 1.5em;
      border-radius: 8px;
      margin: 2em 0;
      border-left: 4px solid #007cba;
    }}
    .research-interests h3 {{
      margin-top: 0;
      color: #007cba;
    }}
    .research-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5em;
      margin-top: 1em;
    }}
    .research-tag {{
      background: #007cba;
      color: white;
      padding: 0.3em 0.8em;
      border-radius: 15px;
      font-size: 0.9em;
    }}
    .articles-container {{
      margin-top: 1em;
    }}
    .load-more-container {{
      text-align: center;
      margin-top: 2em;
      padding: 1.5em;
      background: #f8f9fa;
      border-radius: 8px;
    }}
    .load-more-btn {{
      background: #007cba;
      color: white;
      border: none;
      padding: 0.8em 2em;
      border-radius: 5px;
      cursor: pointer;
      font-size: 1em;
      font-weight: 500;
      transition: all 0.2s;
      margin-bottom: 1em;
    }}
    .load-more-btn:hover {{
      background: #005a87;
      transform: translateY(-1px);
      box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }}
    .load-more-btn:disabled {{
      background: #6c757d;
      cursor: not-allowed;
      transform: none;
      box-shadow: none;
    }}
    .articles-count {{
      display: block;
      color: #666;
      font-size: 0.9em;
      font-style: italic;
    }}
    .hidden {{
      display: none;
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
      .research-tags {{
        justify-content: center;
      }}
    }}
  </style>
</head>
<body>
  <header class="site-header">
    <div class="container">
      <a class="brand" href="./index.html">Apiros3</a>
      <button class="nav-toggle" onclick="toggleNav()">☰</button>
    </div>
    <nav class="nav-menu" id="navMenu">
      <div class="container">
        {nav_menu}
      </div>
    </nav>
  </header>
  <script>
    let articlesPerLoad = 5;
    let currentlyVisible = 5;
    let allArticles = [];

    function toggleNav() {{
      const nav = document.getElementById('navMenu');
      nav.classList.toggle('show');
    }}
    
    function initializeLoadMore() {{
      const articlesList = document.getElementById('articlesList');
      allArticles = Array.from(articlesList.children);
      
      // Hide all articles initially
      allArticles.forEach((article, index) => {{
        if (index >= currentlyVisible) {{
          article.style.display = 'none';
        }}
      }});
      
      updateLoadMoreButton();
    }}
    
    function loadMoreArticles() {{
      const newVisibleCount = currentlyVisible + articlesPerLoad;
      
      // Show more articles
      for (let i = currentlyVisible; i < newVisibleCount && i < allArticles.length; i++) {{
        allArticles[i].style.display = 'flex';
      }}
      
      currentlyVisible = Math.min(newVisibleCount, allArticles.length);
      updateLoadMoreButton();
    }}
    
    function updateLoadMoreButton() {{
      const loadMoreBtn = document.getElementById('loadMoreBtn');
      const articlesCount = document.getElementById('articlesCount');
      
      if (currentlyVisible >= allArticles.length) {{
        loadMoreBtn.disabled = true;
        loadMoreBtn.textContent = 'All Articles Loaded';
        articlesCount.textContent = `Showing all ${{allArticles.length}} articles`;
      }} else {{
        loadMoreBtn.disabled = false;
        loadMoreBtn.textContent = `Load ${{Math.min(articlesPerLoad, allArticles.length - currentlyVisible)}} More Articles`;
        articlesCount.textContent = `Showing ${{currentlyVisible}} of ${{allArticles.length}} articles`;
      }}
    }}
    
    // Initialize load more when page loads
    document.addEventListener('DOMContentLoaded', initializeLoadMore);
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
      <p>Welcome to my academic portfolio. I am a research scientist working at the intersection of mathematics and computer science. My research focuses on algebraic structures, formal methods, and theoretical computer science, with particular emphasis on the connections between algebra and logic in computational systems.</p>
      
      <div class="research-interests">
        <h3>Research Interests</h3>
        <p>My work spans several interconnected areas:</p>
        <div class="research-tags">
          <span class="research-tag">Algebraic Number Theory</span>
          <span class="research-tag">Formal Methods</span>
          <span class="research-tag">Type Theory</span>
          <span class="research-tag">Commutative Algebra</span>
          <span class="research-tag">Galois Theory</span>
          <span class="research-tag">Proof Assistants</span>
          <span class="research-tag">Category Theory</span>
          <span class="research-tag">Computational Logic</span>
        </div>
      </div>
    </section>

    <section class="content-section">
      <h2>Recent Articles</h2>
      <div class="articles-container">
        <ul class="post-list" id="articlesList">
          {''.join(all_items)}
        </ul>
        <div class="load-more-container">
          <button id="loadMoreBtn" onclick="loadMoreArticles()" class="load-more-btn">Load More Articles</button>
          <span id="articlesCount" class="articles-count">Showing 5 of {len(posts)} articles</span>
        </div>
      </div>
    </section>

{publications_html}
    
    <section class="content-section">
      <div class="contact-section">
        <h3>Contact & Information</h3>
        <div class="contact-info">
          <p><strong>Email:</strong> your.email@institution.edu</p>
          <p><strong>Institution:</strong> [Your Institution]</p>
          <p><strong>Department:</strong> Mathematics & Computer Science</p>
          <p><strong>Research Focus:</strong> Algebraic structures, formal methods, and computational logic</p>
          <p><strong>Location:</strong> [Your Location]</p>
        </div>
      </div>
    </section>
  </main>
</body>
</html>"""

def build_blog_listing(posts):
    """Build a simple blog listing page with all articles."""
    
    # Generate article items
    all_items = []
    for post in posts:
        tags_html = ""
        if post["tags"]:
            tags_html = f"""
            <div class="post-tags">
              {''.join(f'<span class="post-tag">{tag}</span>' for tag in post["tags"])}
            </div>"""
        
        abstract_html = ""
        if post.get("abstract"):
            abstract_html = f'<div class="post-abstract">{post["abstract"]}</div>'
        
        all_items.append(f"""
        <li class="post-item">
          <div class="post-header">
            <a href="posts/{post["slug"]}/index.html" class="post-title">{post["title"]}</a>
            <a href="../pdf/{post["slug"]}.pdf" class="post-download" target="_blank">PDF</a>
          </div>
          <div class="post-meta">
            <span class="post-date">{post["date"]}</span>
            {tags_html}
          </div>
          {abstract_html}
        </li>""")
    
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>All Articles - Apiros3</title>
  <link rel="stylesheet" href="../asset/main.css">
  <style>
    .hero {{
      background: linear-gradient(135deg, #007cba 0%, #005a87 100%);
      color: white;
      padding: 2em 0;
      text-align: center;
      margin-bottom: 2em;
    }}
    .hero h1 {{
      font-size: 2.5em;
      margin: 0 0 0.5em 0;
      font-weight: 300;
    }}
    .hero p {{
      font-size: 1.1em;
      margin: 0;
      opacity: 0.9;
    }}
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
      flex-direction: column;
      transition: box-shadow 0.2s;
    }}
    .post-item:hover {{
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    .post-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 0.5em;
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
    .post-abstract {{
      color: #555;
      font-size: 0.95em;
      line-height: 1.5;
      margin: 0.5em 0 1em 0;
      font-style: italic;
    }}
    .post-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.3em;
      margin-top: 0.5em;
    }}
    .post-tag {{
      background: linear-gradient(135deg, #FF6B6B 0%, #E53E3E 100%);
      color: white;
      padding: 0.4em 0.9em;
      border-radius: 15px;
      font-size: 0.85em;
      font-weight: 700;
      border: 2px solid #C53030;
      transition: all 0.3s ease;
      display: inline-block;
      margin: 0.15em;
      text-transform: lowercase;
      letter-spacing: 0.5px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.15);
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
    @media (max-width: 768px) {{
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
</head>
<body>
  <header class="site-header">
    <div class="container">
      <a class="brand" href="../index.html">Apiros3</a>
    </div>
  </header>

  <div class="hero">
    <div class="container">
      <h1>All Articles</h1>
      <p>Complete list of research articles and notes</p>
    </div>
  </div>

  <main class="container">
    <a href="../index.html" class="back-link">← Back to Portfolio</a>
    
    <ul class="post-list">
      {''.join(all_items)}
    </ul>
  </main>
</body>
</html>"""

def build_publications_page():
    """Build a dedicated publications page with rich metadata."""
    
    import json
    from pathlib import Path
    
    # Read publication metadata
    publications = []
    pub_dir = Path("Notes/publication")
    if pub_dir.exists():
        for meta_file in pub_dir.glob("*.meta.json"):
            with open(meta_file, "r", encoding="utf-8") as f:
                pub_data = json.load(f)
                publications.append(pub_data)
    
    # Sort by year (newest first)
    publications.sort(key=lambda p: int(p.get("year", "0")), reverse=True)
    
    # Generate publication items
    pub_items = []
    for pub in publications:
        title = pub.get("title", "Untitled")
        authors = pub.get("authors", [])
        conference = pub.get("conference", "Unknown")
        year = pub.get("year", "Unknown")
        abstract = pub.get("abstract", "")
        arxiv = pub.get("arxiv", "")
        doi = pub.get("doi", "")
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
        
        # Check if PDF exists
        pdf_filename = meta_file.stem.replace(".meta", "") + ".pdf"
        pdf_path = pub_dir / pdf_filename
        if pdf_path.exists():
            links_html += f'<a href="../Notes/publication/{pdf_filename}" class="pub-link pdf-link" target="_blank">PDF</a>'
        
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
    .hero {{
      background: linear-gradient(135deg, #007cba 0%, #005a87 100%);
      color: white;
      padding: 2em 0;
      text-align: center;
      margin-bottom: 2em;
    }}
    .hero h1 {{
      font-size: 2.5em;
      margin: 0 0 0.5em 0;
      font-weight: 300;
    }}
    .hero p {{
      font-size: 1.1em;
      margin: 0;
      opacity: 0.9;
    }}
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
    .site-header {{
      background: #fff;
      border-bottom: 1px solid #e9ecef;
      padding: 1rem 0;
      margin-bottom: 0;
      position: sticky;
      top: 0;
      z-index: 1000;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}
    .site-header .container {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .brand {{
      color: #333;
      text-decoration: none;
      font-size: 1.5em;
      font-weight: 700;
      letter-spacing: -0.5px;
    }}
    .brand:hover {{
      color: #007cba;
    }}
    .main-nav {{
      display: flex;
      align-items: center;
    }}
    .nav-list {{
      display: flex;
      list-style: none;
      margin: 0;
      padding: 0;
      gap: 2rem;
    }}
    .nav-item {{
      margin: 0;
    }}
    .nav-link {{
      color: #333;
      text-decoration: none;
      font-weight: 500;
      font-size: 0.95em;
      padding: 0.5rem 0;
      transition: color 0.2s ease;
      position: relative;
    }}
    .nav-link:hover, .nav-link.current {{
      color: #007cba;
    }}
    .nav-link::after {{
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      width: 0;
      height: 2px;
      background: #007cba;
      transition: width 0.3s ease;
    }}
    .nav-link:hover::after, .nav-link.current::after {{
      width: 100%;
    }}
    .nav-toggle {{
      display: none;
      background: none;
      border: none;
      font-size: 1.2em;
      cursor: pointer;
      color: #333;
      padding: 0.5rem;
    }}
    @media (max-width: 768px) {{
      .nav-toggle {{
        display: block;
      }}
      .main-nav {{
        display: none;
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: #fff;
        border-top: 1px solid #e9ecef;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
      }}
      .main-nav.show {{
        display: block;
      }}
      .nav-list {{
        flex-direction: column;
        gap: 0;
        padding: 1rem 0;
      }}
      .nav-item {{
        border-bottom: 1px solid #f0f0f0;
      }}
      .nav-item:last-child {{
        border-bottom: none;
      }}
      .nav-link {{
        display: block;
        padding: 1rem 2rem;
        color: #333;
      }}
      .nav-link::after {{
        display: none;
      }}
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
    <a href="../index.html" class="back-link">← Back to Portfolio</a>
    
    <ul class="publication-list">
      {''.join(pub_items)}
    </ul>
  </main>
</body>
</html>"""

def main():
    print("Starting portfolio generation...")
    posts = []
    for tex in POSTS_SRC.glob("*.tex"):
        date_str, slug = parse_name(tex)
        meta = read_meta(slug)
        title = meta.get("title") or slug.replace("-", " ").title()
        tags  = meta.get("tags", [])
        abstract = meta.get("abstract", "")
        # Only include if HTML output exists (PDF is optional)
        html_path = POSTS_OUT / slug / "index.html"
        if html_path.exists():
            posts.append({
                "date": date_str, "slug": slug,
                "title": title, "tags": tags, "abstract": abstract
            })
            print(f"Found article: {title} - Abstract: {abstract[:50]}...")
    
    print(f"Total articles found: {len(posts)}")
    index_html = build_index(posts)
    
    # Create root index.html
    Path("index.html").write_text(index_html, encoding="utf-8")
    print("Generated index.html")
    
    # Create blog listing page
    blog_listing_html = build_blog_listing(posts)
    (BUILD / "index.html").write_text(blog_listing_html, encoding="utf-8")
    print("Generated build/index.html")
    
    # Create publications page
    publications_html = build_publications_page()
    (BUILD / "publications.html").write_text(publications_html, encoding="utf-8")
    print("Generated build/publications.html")

if __name__ == "__main__":
    main()
