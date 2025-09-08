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
    ABOUT_PROFILE_PICTURE, ABOUT_PROFILE_ALT, NAV_BRAND, NAV_ITEMS
)


def generate_main_index(posts: List[Dict[str, Any]]) -> str:
    """Generate the main index page."""
    return f"""{generate_html_head(f"{SITE_TITLE} - Academic Portfolio")}
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
          <p>{ABOUT_CONTENT}</p>
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
