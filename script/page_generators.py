"""
Page generators for different types of pages.
"""
from pathlib import Path
from typing import List, Dict, Any
from .template_engine import (
    generate_html_head, generate_navigation, generate_hero, 
    generate_contact_sidebar, generate_contact_footer, generate_nav_script,
    generate_publication_item, generate_talk_item, generate_tag_filters, generate_tag_filter_script
)
from .config import (
    SITE_TITLE, SITE_DESCRIPTION, ABOUT_TITLE, ABOUT_CONTENT, 
    ABOUT_PROFILE_PICTURE, ABOUT_PROFILE_ALT, NAV_BRAND, NAV_ITEMS,
    NOTES_TITLE, NOTES_DESCRIPTION, READING_LIST_TITLE, READING_LIST_DESCRIPTION
)


def format_about_content(content: str) -> str:
    """Format about content to support multiple paragraphs."""
    if not content:
        return ""
    
    # Split content by double newlines to create paragraphs
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
    
    if not paragraphs:
        return ""
    
    # Wrap each paragraph in <p> tags
    formatted_paragraphs = [f"<p>{paragraph}</p>" for paragraph in paragraphs]
    
    return '\n          '.join(formatted_paragraphs)


def generate_main_index(posts: List[Dict[str, Any]]) -> str:
    """Generate the main index page."""
    return f"""{generate_html_head(f"{SITE_TITLE} - Homepage")}
<body>
{generate_navigation("about")}

  <main class="container">
    <div class="main-layout">
      <div class="main-content">
        <section class="content-section" id="about">
          <div class="about-header">
            <h2>{ABOUT_TITLE}</h2>
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
          <a href="{post["slug"]}/index.html" class="post-item">
            <div class="post-header">
              <div class="post-title">{post["title"]}</div>
              {pdf_link}
            </div>
            {abstract_html}
            <div class="post-meta">
              <span class="post-date">{post["date"]}</span>
              {tags_html}
            </div>
          </a>
        </li>""")
    
    return f"""{generate_html_head(f"Blog - {SITE_TITLE}", base_path="../")}
<body class="blog-page">
{generate_navigation("blog", "../")}

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
    # Generate publication items
    pub_items = []
    for pub in publications:
        pub_items.append(generate_publication_item(pub, "../"))
    
    # Generate talk items
    talk_items = []
    for talk in talks:
        talk_items.append(generate_talk_item(talk, "../"))
    
    return f"""{generate_html_head(f"Publications - {SITE_TITLE}", base_path="../")}
<body class="publications-page">
{generate_navigation("publications", "../")}

  <main class="container">
    <h2 class="section-title">Publications</h2>
    <ul class="publication-list">
      {''.join(pub_items)}
    </ul>
    
    <h2 class="section-title">Talks & Presentations</h2>
    <ul class="publication-list">
      {''.join(talk_items)}
    </ul>
  </main>
{generate_nav_script()}
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
        # Format author and year
        author_year = f"{item['author']} ({item['year']})"
        
        # Format status with appropriate styling
        status_class = f"status-{item['status'].replace('-', '_')}"
        status_text = item['status'].replace('-', ' ').title()
        
        # Format type
        type_text = item['type'].title()
        
        reading_items.append(f"""
      <li class="reading-item">
        <div>
          <div class="reading-title">{item['title']}</div>
          <div class="reading-meta">
            <span class="reading-author">{author_year}</span>
            <span class="reading-type">{type_text}</span>
            <span class="reading-status {status_class}">{status_text}</span>
          </div>
          <div class="reading-description">{item['description']}</div>
        </div>
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
