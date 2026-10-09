"""
Template engine for generating HTML pages.
"""
from pathlib import Path
from html import escape
import re
from typing import List, Dict, Any
from .config import (
    SITE_TITLE, SITE_DESCRIPTION, SITE_AUTHOR, SITE_EMAIL, 
    SITE_INSTITUTION, SITE_DEPARTMENT, SITE_LOCATION,
    CSS_FILES, KATEX_CSS, KATEX_JS, KATEX_AUTO_RENDER, MATH_DELIMITERS,
    NAV_BRAND, NAV_ITEMS, PUB_LINK_COLORS
)


def generate_html_head(title: str, css_files: List[str] = None, include_math: bool = False, base_path: str = "", description: str = None, canonical_url: str = "", extra_head: str = "") -> str:
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
    
    canonical_link = f'  <link rel="canonical" href="{escape(canonical_url, quote=True)}">\n' if canonical_url else ""

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(SITE_DESCRIPTION if description is None else description, quote=True)}"/>
{canonical_link}{extra_head}{css_links}{math_links}{math_script}
</head>"""


def generate_navigation(current_page: str = "about", base_path: str = "") -> str:
    """Generate navigation menu."""
    nav_items = []
    for item in NAV_ITEMS:
        path = item["url"].removeprefix("./")
        page = "about" if path == "index.html" else path.split("/")[0]
        is_current = page == current_page
        current_class = " current" if is_current else ""
        current_aria = ' aria-current="page"' if is_current else ''
        # Adjust URLs based on base_path
        if base_path and not item["url"].startswith("http"):
            if item["url"].startswith("./"):
                item_url = base_path + item["url"][2:]  # Remove "./" and add base_path
            else:
                item_url = base_path + item["url"]
        else:
            item_url = item["url"]
        nav_items.append(f'<li class="nav-item"><a href="{item_url}" class="nav-link{current_class}"{current_aria}>{item["name"]}</a></li>')
    
    # Adjust brand link based on base_path
    brand_link = base_path + "index.html" if base_path else "./index.html"
    
    return f"""  <header class="site-header">
    <div class="container">
      <a class="brand" href="{brand_link}">{NAV_BRAND}</a>
      <nav class="main-nav" id="main-navigation" aria-label="Primary navigation">
        <ul class="nav-list">
          {''.join(nav_items)}
        </ul>
      </nav>
      <button class="nav-toggle" type="button" aria-label="Toggle navigation" aria-controls="main-navigation" aria-expanded="false" onclick="toggleNav()">☰</button>
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
    department_html = f'<p><strong>Department:</strong><br>{SITE_DEPARTMENT}</p>' if SITE_DEPARTMENT else ''
    return f"""      <div class="sidebar">
        <h3>Contact</h3>
        <div class="contact-info-sidebar">
          <p><strong>Email:</strong><br>{SITE_EMAIL}</p>
          <p><strong>Institution:</strong><br>{SITE_INSTITUTION}</p>
          {department_html}
          <p><strong>Location:</strong><br>{SITE_LOCATION}</p>
        </div>
      </div>"""


def generate_contact_footer() -> str:
    """Generate contact information footer."""
    department_html = f"""        <div class="contact-item">
          <strong>Department:</strong><span class="contact-value">{SITE_DEPARTMENT}</span>
        </div>""" if SITE_DEPARTMENT else ''
    return f"""  <footer class="contact-footer">
    <div class="container">
      <h3>Contact</h3>
      <div class="contact-info-footer">
        <div class="contact-item">
          <strong>Email:</strong><span class="contact-value">{SITE_EMAIL}</span>
        </div>
        <div class="contact-item">
          <strong>Institution:</strong><span class="contact-value">{SITE_INSTITUTION}</span>
        </div>
        {department_html}
        <div class="contact-item">
          <strong>Location:</strong><span class="contact-value">{SITE_LOCATION}</span>
        </div>
      </div>
    </div>
  </footer>"""


def generate_nav_script() -> str:
    """Generate navigation toggle script."""
    return """  <script>
    function toggleNav() {
      const nav = document.querySelector('.main-nav');
      const expanded = nav.classList.toggle('show');
      document.querySelector('.nav-toggle').setAttribute('aria-expanded', String(expanded));
    }
    document.addEventListener('keydown', function(event) {
      const nav = document.querySelector('.main-nav');
      if (event.key === 'Escape' && nav.classList.contains('show')) {
        toggleNav();
        document.querySelector('.nav-toggle').focus();
      }
    });
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


def generate_abstract_toggle(abstract: str, panel_id: str) -> tuple[str, str]:
    """Generate a button and initially hidden abstract when text is available."""
    if not abstract or not abstract.strip():
        return "", ""
    button = f'<button type="button" class="abstract-toggle" aria-expanded="false" aria-controls="{panel_id}" onclick="toggleAbstract(this)">Abstract</button>'
    panel = f'<p id="{panel_id}" class="publication-abstract" hidden>{escape(abstract)}</p>'
    return button, panel


def generate_abstract_script() -> str:
    """Keep abstract visibility and the button's expanded state in sync."""
    return """  <script>
    function toggleAbstract(button) {
      const panel = document.getElementById(button.getAttribute('aria-controls'));
      const expanded = button.getAttribute('aria-expanded') === 'true';
      panel.hidden = expanded;
      button.setAttribute('aria-expanded', String(!expanded));
      button.textContent = expanded ? 'Abstract' : 'Hide abstract';
    }
  </script>"""


def generate_publication_item(pub: Dict[str, Any], base_path: str = "", abstract_id: str = "publication-abstract") -> str:
    """Generate a single publication item."""
    title = pub.get("title", "Untitled")
    authors = pub.get("authors", [])
    conference = pub.get("conference", "Unknown")
    year = pub.get("year", "Unknown")
    arxiv = pub.get("arxiv", "")
    doi = pub.get("doi", "")
    code = pub.get("code", "")
    venue = pub.get("venue", "")
    pages = pub.get("pages", "")
    abstract_button, abstract_panel = generate_abstract_toggle(pub.get("abstract", ""), abstract_id)
    
    # Format authors
    if isinstance(authors, list):
        authors_str = ", ".join(authors)
    else:
        authors_str = str(authors)
    
    # Format venue info
    venue_info = venue or conference
    if year:
        venue_info += f", {year}"
    
    # Generate links
    links_html = ""
    if doi:
        identifier = re.search(r'10\.\d{4,9}/[^?#\s]+', doi)
        label = f"DOI: {identifier.group(0)}" if identifier else "DOI"
        links_html += f'<a href="{escape(doi, quote=True)}" class="pub-link doi-link" target="_blank">{escape(label)}</a>'
    if arxiv:
        links_html += f'<a href="{arxiv}" class="pub-link arxiv-link" target="_blank">arXiv</a>'
    if code:
        links_html += f'<a href="{code}" class="pub-link code-link" target="_blank">Code</a>'
    
    # Prefer the explicit PDF, then look for this paper's matching filename.
    pdf = pub.get("pdf", "")
    if not pdf and pub.get("filename"):
        for directory in ("publications/data", "posts", "Notes/publication"):
            pdf_path = Path(directory) / f"{pub['filename']}.pdf"
            if pdf_path.exists():
                pdf = pdf_path.as_posix()
                break
    if pdf:
        links_html += f'<a href="{escape(base_path + pdf, quote=True)}" class="pub-link pdf-link" target="_blank">PDF</a>'

    title_html = escape(title)
    if pub.get("landing_page"):
        title_html = f'<a href="{escape(base_path + pub["landing_page"], quote=True)}">{title_html}</a>'
    
    return f"""
        <li class="publication-item">
          <h3 class="publication-title">{title_html}</h3>
          <div class="publication-authors">{escape(authors_str)}</div>
          <div class="publication-venue">{escape(venue_info)}</div>
          <div class="publication-links">{links_html}{abstract_button}</div>{f'<div class="publication-pages">{escape(pages)}</div>' if pages else ''}{abstract_panel}
        </li>"""


def generate_talk_item(talk: Dict[str, Any], base_path: str = "", abstract_id: str = "talk-abstract") -> str:
    """Generate a single talk item."""
    title = talk.get("title", "Untitled")
    venue = talk.get("venue", "Unknown")
    location = talk.get("location", "")
    date = talk.get("date", "")
    year = talk.get("year", "")
    slides = talk.get("slides", "")
    video = talk.get("video", "")
    coauthors = talk.get("coauthors", [])
    talk_type = talk.get("type", "talk")
    abstract_button, abstract_panel = generate_abstract_toggle(talk.get("abstract", ""), abstract_id)
    
    # Format venue info
    venue_info = venue
    if location:
        venue_info += f", {location}"
    if date:
        venue_info += f", {date}"
    
    # Format coauthors
    coauthors_str = ""
    if coauthors and isinstance(coauthors, list) and len(coauthors) > 0:
        coauthors_str = f"with {', '.join(coauthors)}"
    
    # Keep presentation details and resources on one compact line.
    details_html = f'<span class="talk-type">{escape(talk_type.title())}</span>'
    if coauthors_str:
        details_html += f'<span class="publication-coauthors">{escape(coauthors_str)}</span>'

    # Generate links
    links_html = ""
    if slides:
        links_html += f'<a href="{slides}" class="pub-link slides-link" target="_blank">Slides</a>'
    if video:
        links_html += f'<a href="{video}" class="pub-link video-link" target="_blank">Video</a>'
    
    return f"""
        <li class="publication-item talk-item">
          <h3 class="publication-title">{escape(title)}</h3>
          <div class="publication-venue">{escape(venue_info)}</div>
          <div class="publication-links">{details_html}{links_html}{abstract_button}</div>{abstract_panel}
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
      const postItems = document.querySelectorAll('.post-list li');
      
      filterButtons.forEach(button => {
        button.addEventListener('click', function() {
          const selectedTag = this.getAttribute('data-tag');
          
          // Update active button
          filterButtons.forEach(btn => btn.classList.remove('active'));
          this.classList.add('active');
          
          // Filter posts
          postItems.forEach(item => {
            const itemTags = item.getAttribute('data-tags');
            if (selectedTag === 'all' || (itemTags && itemTags.trim() !== '' && itemTags.includes(selectedTag))) {
              item.classList.remove('hidden');
            } else {
              item.classList.add('hidden');
            }
          });
        });
      });
    });
  </script>"""
