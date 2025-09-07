"""
Template engine for generating HTML pages.
"""
from pathlib import Path
from typing import List, Dict, Any
from .config import (
    SITE_TITLE, SITE_DESCRIPTION, SITE_AUTHOR, SITE_EMAIL, 
    SITE_INSTITUTION, SITE_DEPARTMENT, SITE_LOCATION,
    CSS_FILES, KATEX_CSS, KATEX_JS, KATEX_AUTO_RENDER, MATH_DELIMITERS,
    NAV_ITEMS, PUB_LINK_COLORS
)


def generate_html_head(title: str, css_files: List[str] = None, include_math: bool = False, base_path: str = "") -> str:
    """Generate HTML head section."""
    if css_files is None:
        css_files = CSS_FILES
    
    css_links = ""
    for css_file in css_files:
        css_links += f'  <link rel="stylesheet" href="{base_path}{css_file}">\n'
    
    math_links = ""
    math_script = ""
    if include_math:
        math_links = f'''  <link rel="stylesheet" href="{KATEX_CSS}">
  <script defer src="{KATEX_JS}"></script>
  <script defer src="{KATEX_AUTO_RENDER}"></script>'''
        
        math_script = f'''
  <script>
    document.addEventListener("DOMContentLoaded", function() {{
      renderMathInElement(document.body, {{
        delimiters: {MATH_DELIMITERS}
      }});
    }});
  </script>'''
    
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>{title}</title>
{css_links}{math_links}{math_script}
</head>"""


def generate_navigation(current_page: str = "about", base_path: str = "") -> str:
    """Generate navigation menu."""
    nav_items = []
    for item in NAV_ITEMS:
        current_class = " current" if item["name"].lower() == current_page else ""
        # Adjust URLs based on base_path
        if base_path and not item["url"].startswith("http"):
            if item["url"].startswith("./"):
                item_url = base_path + item["url"][2:]  # Remove "./" and add base_path
            else:
                item_url = base_path + item["url"]
        else:
            item_url = item["url"]
        nav_items.append(f'<li class="nav-item"><a href="{item_url}" class="nav-link{current_class}">{item["name"]}</a></li>')
    
    # Adjust brand link based on base_path
    brand_link = base_path + "index.html" if base_path else "./index.html"
    
    return f"""  <header class="site-header">
    <div class="container">
      <a class="brand" href="{brand_link}">{SITE_TITLE}</a>
      <nav class="main-nav">
        <ul class="nav-list">
          {''.join(nav_items)}
        </ul>
      </nav>
      <button class="nav-toggle" onclick="toggleNav()">☰</button>
    </div>
  </header>"""


def generate_hero(title: str, subtitle: str) -> str:
    """Generate hero section."""
    return f"""  <div class="hero">
    <div class="container">
      <h1>{title}</h1>
      <p>{subtitle}</p>
    </div>
  </div>"""


def generate_contact_sidebar() -> str:
    """Generate contact information sidebar."""
    return f"""      <div class="sidebar">
        <h3>Contact</h3>
        <div class="contact-info-sidebar">
          <p><strong>Email:</strong><br>{SITE_EMAIL}</p>
          <p><strong>Institution:</strong><br>{SITE_INSTITUTION}</p>
          <p><strong>Department:</strong><br>{SITE_DEPARTMENT}</p>
          <p><strong>Location:</strong><br>{SITE_LOCATION}</p>
        </div>
      </div>"""


def generate_nav_script() -> str:
    """Generate navigation toggle script."""
    return """  <script>
    function toggleNav() {
      const nav = document.querySelector('.main-nav');
      nav.classList.toggle('show');
    }
  </script>"""


def generate_post_item(post: Dict[str, Any], base_path: str = "") -> str:
    """Generate a single post item."""
    pdf_link = f'<a href="{base_path}pdf/{post["slug"]}.pdf" class="post-download" target="_blank">PDF</a>' if post.get("has_pdf", False) else ''
    
    return f"""
        <li class="post-item">
          <a href="{base_path}posts/{post["slug"]}/index.html" class="post-title">{post["title"]}</a>
          <span class="post-date">{post["date"]}</span>
          {pdf_link}
        </li>"""


def generate_publication_item(pub: Dict[str, Any], base_path: str = "") -> str:
    """Generate a single publication item."""
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
    
    # Check for PDF
    pub_dir = Path("publications/data")
    meta_files = list(pub_dir.glob("*.meta.json"))
    pdf_found = False
    
    for pdf_name in [f"{pub.get('filename', 'itp25')}.pdf", "itp25.pdf"]:
        pdf_path = Path("posts") / pdf_name
        if pdf_path.exists():
            links_html += f'<a href="../posts/{pdf_name}" class="pub-link pdf-link" target="_blank">PDF</a>'
            pdf_found = True
            break
    
    if not pdf_found:
        for pdf_name in [f"{pub.get('filename', 'itp25')}.pdf", "itp25.pdf"]:
            pdf_path = Path("Notes/publication") / pdf_name
            if pdf_path.exists():
                links_html += f'<a href="../Notes/publication/{pdf_name}" class="pub-link pdf-link" target="_blank">PDF</a>'
                pdf_found = True
                break
    
    return f"""
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
        </li>"""


def generate_tag_filters(posts: List[Dict[str, Any]]) -> str:
    """Generate tag filter buttons."""
    all_tags = set()
    for post in posts:
        all_tags.update(post["tags"])
    all_tags = sorted(list(all_tags))
    
    tag_buttons = ['<button class="tag-filter active" data-tag="all">All</button>']
    for tag in all_tags:
        tag_buttons.append(f'<button class="tag-filter" data-tag="{tag}">{tag.title()}</button>')
    
    return f"""    <div class="filter-section">
      <h3>Filter by Tag</h3>
      <div class="tag-filters">
        {''.join(tag_buttons)}
      </div>
    </div>"""


def generate_tag_filter_script() -> str:
    """Generate JavaScript for tag filtering."""
    return """  <script>
    // Tag filtering functionality
    document.addEventListener('DOMContentLoaded', function() {
      const filterButtons = document.querySelectorAll('.tag-filter');
      const postItems = document.querySelectorAll('.post-item');
      
      filterButtons.forEach(button => {
        button.addEventListener('click', function() {
          const selectedTag = this.getAttribute('data-tag');
          
          // Update active button
          filterButtons.forEach(btn => btn.classList.remove('active'));
          this.classList.add('active');
          
          // Filter posts
          postItems.forEach(item => {
            const itemTags = item.getAttribute('data-tags');
            if (selectedTag === 'all' || (itemTags && itemTags.includes(selectedTag))) {
              item.classList.remove('hidden');
            } else {
              item.classList.add('hidden');
            }
          });
        });
      });
    });
  </script>"""
