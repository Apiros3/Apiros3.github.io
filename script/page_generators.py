"""
Page generators for different types of pages.
"""
from pathlib import Path
from typing import List, Dict, Any
from .template_engine import (
    generate_html_head, generate_navigation, generate_hero, 
    generate_contact_sidebar, generate_nav_script, generate_post_item,
    generate_publication_item, generate_tag_filters, generate_tag_filter_script
)
from .config import SITE_TITLE, SITE_DESCRIPTION


def generate_main_index(posts: List[Dict[str, Any]]) -> str:
    """Generate the main index page."""
    # Generate recent posts (first 5)
    recent_items = []
    for post in posts[:5]:
        recent_items.append(generate_post_item(post, ""))
    
    return f"""{generate_html_head(f"{SITE_TITLE} - Academic Portfolio")}
<body>
{generate_navigation("about")}

{generate_hero(SITE_TITLE, "Research Scientist, Mathematics & Computer Science")}

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
              <a href="build/index.html" class="load-more-btn">View All Articles</a>
            </div>
          </div>
        </section>
      </div>
      
{generate_contact_sidebar()}
    </div>
  </main>
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
    
    return f"""{generate_html_head(f"Blog - {SITE_TITLE}")}
<body>
{generate_navigation("blog")}

{generate_hero("Blog", "Complete list of blog posts and research notes")}

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


def generate_publications_page(publications: List[Dict[str, Any]]) -> str:
    """Generate the publications page."""
    # Generate publication items
    pub_items = []
    for pub in publications:
        pub_items.append(generate_publication_item(pub, "../"))
    
    return f"""{generate_html_head(f"Publications - {SITE_TITLE}")}
<body>
{generate_navigation("publications")}

{generate_hero("Publications", "Research papers and academic publications")}

  <main class="container">
    <a href="../index.html" class="back-link">← Back to Mainpage</a>
    
    <ul class="publication-list">
      {''.join(pub_items)}
    </ul>
  </main>
{generate_nav_script()}
</body>
</html>"""
