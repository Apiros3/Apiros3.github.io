"""
Page generators for different types of pages.
"""
from pathlib import Path
from html import escape
from typing import List, Dict, Any
from .template_engine import (
    generate_html_head, generate_navigation, generate_hero, 
    generate_contact_sidebar, generate_contact_footer, generate_nav_script,
    generate_publication_item, generate_talk_item, generate_tag_filters, generate_tag_filter_script,
    generate_abstract_script
)
from .config import (
    SITE_TITLE, SITE_DESCRIPTION, SITE_URL, ABOUT_TITLE, ABOUT_CONTENT,
    ABOUT_PROFILE_PICTURE, ABOUT_PROFILE_ALT, ABOUT_SUBTITLE, ABOUT_AFFILIATION, NAV_BRAND, NAV_ITEMS,
    NOTES_TITLE, NOTES_DESCRIPTION, READING_LIST_TITLE, READING_LIST_DESCRIPTION
)


def format_about_content(content: str) -> str:
    """Format about content to support multiple paragraphs and convert markdown links."""
    if not content:
        return ""
    
    # Split content by double newlines to create paragraphs
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
    
    if not paragraphs:
        return ""
    
    # Convert markdown links to HTML and wrap each paragraph in <p> tags
    import re
    
    def convert_markdown_links(text):
        """Convert markdown links [text](url) to HTML <a> tags."""
        # Pattern to match markdown links: [text](url)
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        return re.sub(link_pattern, r'<a href="\2">\1</a>', text)
    
    formatted_paragraphs = []
    for paragraph in paragraphs:
        heading = re.fullmatch(r'(#{2,3})\s+([^\n]+)', paragraph)
        if heading:
            level = len(heading.group(1))
            formatted_paragraphs.append(f"<h{level}>{escape(heading.group(2))}</h{level}>")
            continue
        # Convert markdown links to HTML
        paragraph = convert_markdown_links(paragraph)
        # Wrap in <p> tags
        formatted_paragraphs.append(f"<p>{paragraph}</p>")
    
    return '\n          '.join(formatted_paragraphs)


def generate_main_index(posts: List[Dict[str, Any]]) -> str:
    """Generate the main index page."""
    return f"""{generate_html_head(f"{SITE_TITLE} - Homepage", canonical_url=SITE_URL + "/")}
<body>
{generate_navigation("about")}

  <main class="container">
    <div class="main-layout">
      <div class="main-content">
        <section class="content-section" id="about" aria-labelledby="profile-name">
          <div class="about-header">
            <div>
              <h1 id="profile-name">{escape(ABOUT_TITLE)}</h1>
              {f'<p class="about-subtitle">{escape(ABOUT_SUBTITLE)}</p>' if ABOUT_SUBTITLE else ''}
              {f'<p class="about-affiliation">{escape(ABOUT_AFFILIATION)}</p>' if ABOUT_AFFILIATION else ''}
            </div>
            {f'<img src="{ABOUT_PROFILE_PICTURE}" alt="{ABOUT_PROFILE_ALT}" class="profile-picture">' if ABOUT_PROFILE_PICTURE else ''}
          </div>
          {format_about_content(ABOUT_CONTENT)}
        </section>
      </div>
    </div>
  </main>

{generate_contact_footer()}
{generate_nav_script()}
</body>
</html>"""


def generate_blog_listing(posts: List[Dict[str, Any]]) -> str:
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
        
        pdf_link = f'<a href="{post["slug"]}/{post["slug"]}.pdf" class="post-download" target="_blank">PDF</a>' if post.get("has_pdf", False) else ''
        all_items.append(f"""
        <li data-tags="{','.join(post["tags"])}">
          <div class="post-item">
            <div class="post-header">
              <a href="{post["slug"]}/index.html" class="post-title">{post["title"]}</a>
              {pdf_link}
            </div>
            {abstract_html}
            <div class="post-meta">
              <span class="post-date">{post["date"]}</span>
              {tags_html}
            </div>
          </div>
        </li>""")
    
    return f"""{generate_html_head(f"Blog - {SITE_TITLE}", base_path="../")}
<body class="blog-page">
{generate_navigation("posts", "../")}

  <main class="container">
    <a href="../index.html" class="back-link">← Back to Mainpage</a>
    
{generate_tag_filters(posts)}
    
    <ul class="post-list">
      {''.join(all_items)}
    </ul>
  </main>
{generate_nav_script()}
{generate_tag_filter_script()}
</body>
</html>"""


def generate_publications_page(publications: List[Dict[str, Any]], talks: List[Dict[str, Any]]) -> str:
    """Generate the publications page."""
    # Keep preprints separate from published papers.
    preprint_items = []
    pub_items = []
    for index, pub in enumerate(publications):
        if pub.get("status") == "preprint":
            preprint_items.append(generate_publication_item(pub, "../", f"preprint-abstract-{index}"))
        else:
            pub_items.append(generate_publication_item(pub, "../", f"publication-abstract-{index}"))

    preprints_html = ""
    if preprint_items:
        preprints_html = f"""<h2 class="section-title">Preprints</h2>
    <ul class="publication-list">{''.join(preprint_items)}
    </ul>
    """
    
    # Generate talk items
    talk_items = []
    for index, talk in enumerate(talks):
        talk_items.append(generate_talk_item(talk, "../", f"talk-abstract-{index}"))
    
    return f"""{generate_html_head(f"Publications - {SITE_TITLE}", base_path="../", canonical_url=SITE_URL + "/publications/index.html")}
<body class="publications-page">
{generate_navigation("publications", "../")}

  <main class="container">
    {preprints_html}<h2 class="section-title">Publications</h2>
    <ul class="publication-list">
      {''.join(pub_items)}
    </ul>
    
    <h2 class="section-title">Talks & Presentations</h2>
    <ul class="publication-list">
      {''.join(talk_items)}
    </ul>
  </main>
{generate_nav_script()}
{generate_abstract_script()}
</body>
</html>"""


def generate_notes_page(notes: List[Dict[str, Any]]) -> str:
    """Generate the notes page."""
    # Generate compact note items
    note_items = []
    for note in notes:
        # Handle both single PDF and multiple PDFs
        pdf_links = []
        if "pdf_file" in note:
            pdf_links.append(f'<a href="../Notes/{note["slug"]}/{note["pdf_file"]}" class="note-download" target="_blank">PDF</a>')
        elif "pdf_files" in note:
            for pdf_file in note["pdf_files"]:
                pdf_links.append(f'<a href="../Notes/{note["slug"]}/{pdf_file}" class="note-download" target="_blank">{pdf_file}</a>')
        
        pdf_links_html = " | ".join(pdf_links) if pdf_links else ""
        
        note_items.append(f"""
      <li class="note-item">
        <div>
          <div class="note-title">{note["title"]}</div>
          <div class="note-description">{note["description"]}</div>
        </div>
        <div class="note-downloads">{pdf_links_html}</div>
      </li>""")
    
    return f"""{generate_html_head(f"{NOTES_TITLE} - {SITE_TITLE}", base_path="../")}
<body class="notes-page">
{generate_navigation("notes-page", "../")}

  <main class="container">
    <a href="../index.html" class="back-link">← Back to Mainpage</a>
    
    <h1 class="page-title">{NOTES_TITLE}</h1>
    <p class="page-description">{NOTES_DESCRIPTION}</p>
    
    <ul class="note-list">
      {''.join(note_items)}
    </ul>
  </main>
{generate_nav_script()}
</body>
</html>"""


def generate_reading_list_page(reading_list: List[Dict[str, Any]]) -> str:
    """Generate the reading list page."""
    # Generate reading list items
    reading_items = []
    for item in reading_list:
        venue_year = f"{item.get('venue', '')} {item['year']}".strip()
        if item.get('type') in ('Book', 'PhD thesis'):
            venue_year = f"{item['type']}, {venue_year}"
        
        reading_items.append(f"""
      <li class="reading-item">
        <h2 class="reading-title">{escape(item['title'])}</h2>
        <p class="reading-meta"><span class="reading-author">{escape(item['author'])}</span> · <span class="reading-venue">{escape(venue_year)}</span></p>
      </li>""")
    
    return f"""{generate_html_head(f"{READING_LIST_TITLE} - {SITE_TITLE}", base_path="../")}
<body class="reading-list-page">
{generate_navigation("reading-list", "../")}

  <main class="container">
    <a href="../index.html" class="back-link">← Back to Mainpage</a>
    
    <h1 class="page-title">{READING_LIST_TITLE}</h1>
    <p class="page-description">{READING_LIST_DESCRIPTION}</p>
    
    <ul class="reading-list">
      {''.join(reading_items)}
    </ul>
  </main>
{generate_nav_script()}
</body>
</html>"""
