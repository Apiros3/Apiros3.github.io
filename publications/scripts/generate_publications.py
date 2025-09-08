#!/usr/bin/env python3
"""
Generate publications page from metadata files in the publications repository.
This script is designed to be run from the main repository that includes this as a submodule.
"""
import json
import sys
from pathlib import Path

def build_publications_page():
    """Build a dedicated publications page with rich metadata."""

    # Read publication metadata from the publications submodule
    publications = []
    talks = []
    pub_dir = Path("publications/data")
    print(f"Looking for publications in: {pub_dir}")
    
    if pub_dir.exists():
        meta_files = list(pub_dir.glob("*.meta.json"))
        print(f"Found {len(meta_files)} metadata files: {meta_files}")
        
        for meta_file in meta_files:
            print(f"Reading {meta_file}")
            with open(meta_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                
                # Check if this is a talks file
                if "talks" in data:
                    talks.extend(data["talks"])
                    print(f"Loaded {len(data['talks'])} talks from {meta_file}")
                else:
                    # Regular publication - store with meta_file for PDF lookup
                    data["_meta_file"] = meta_file
                    publications.append(data)
                    print(f"Loaded publication: {data.get('title', 'Untitled')}")
    else:
        print(f"Publication directory does not exist: {pub_dir}")
        return None
    
    # Sort by year (newest first)
    publications.sort(key=lambda p: int(p.get("year", "0")), reverse=True)
    talks.sort(key=lambda t: t.get("date", ""), reverse=True)
    
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
        
        # Check if PDF exists
        meta_file = pub.get("_meta_file")
        if meta_file:
            pdf_filename = meta_file.stem.replace(".meta", "") + ".pdf"
            pdf_path = Path("Notes/publication") / pdf_filename
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
    
    # Generate talk items
    talk_items = []
    for talk in talks:
        title = talk.get("title", "Untitled")
        talk_type = talk.get("type", "talk")
        venue = talk.get("venue", "Unknown")
        location = talk.get("location", "")
        date = talk.get("date", "Unknown")
        year = talk.get("year", "Unknown")
        abstract = talk.get("abstract", "")
        slides = talk.get("slides", "")
        video = talk.get("video", "")
        coauthors = talk.get("coauthors", [])
        
        # Format coauthors
        if isinstance(coauthors, list) and coauthors:
            coauthors_str = ", ".join(coauthors)
        else:
            coauthors_str = ""
        
        # Format venue info
        venue_info = f"{venue}"
        if location:
            venue_info += f", {location}"
        if date:
            # Format date nicely
            try:
                from datetime import datetime
                date_obj = datetime.strptime(date, "%Y-%m-%d")
                formatted_date = date_obj.strftime("%B %d, %Y")
                venue_info += f", {formatted_date}"
            except:
                venue_info += f", {date}"
        
        # Generate links
        links_html = ""
        if slides:
            links_html += f'<a href="{slides}" class="pub-link slides-link" target="_blank">Slides</a>'
        if video:
            links_html += f'<a href="{video}" class="pub-link video-link" target="_blank">Video</a>'
        
        # Format coauthors display
        coauthors_display = ""
        if coauthors_str:
            coauthors_display = f'<div class="publication-coauthors">with {coauthors_str}</div>'
        
        talk_items.append(f"""
        <li class="publication-item talk-item">
          <div class="publication-header">
            <h3 class="publication-title">{title}</h3>
            <div class="publication-links">
              {links_html}
            </div>
          </div>
          <div class="publication-meta">
            <div class="publication-venue">{venue_info}</div>
            <div class="talk-type">{talk_type.title()}</div>
            {coauthors_display}
          </div>
          {f'<div class="publication-abstract">{abstract}</div>' if abstract else ''}
        </li>""")
    
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Publications - Apiros3</title>
  <link rel="stylesheet" href="../css/main.css">
  <style>
    /* Override all hover effects from main CSS */
    .publication-item:hover {{
      background: none !important;
      padding: 0.8em 0 0.8em 0.8em !important;
      border-radius: 0 !important;
      margin: 0.8em 0 !important;
    }}
    .arxiv-link:hover {{
      background: #ff6b35 !important;
    }}
    .doi-link:hover {{
      background: #007cba !important;
    }}
    .pdf-link:hover {{
      background: #28a745 !important;
    }}
    .code-link:hover {{
      background: #6f42c1 !important;
    }}
    .slides-link:hover {{
      background: #17a2b8 !important;
    }}
    .video-link:hover {{
      background: #dc3545 !important;
    }}
    .back-link:hover {{
      text-decoration: none !important;
    }}
    .brand:hover {{
      color: #333 !important;
    }}
    .nav-link:hover {{
      color: #333 !important;
    }}
    .nav-link:hover::after {{
      width: 0 !important;
    }}
    
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
    .publication-list {{
      list-style: none;
      padding: 0;
    }}
    .publication-item {{
      border-left: 3px solid #007cba;
      margin: 0.8em 0;
      padding: 0.8em 0 0.8em 0.8em;
      background: none;
      box-sizing: border-box;
      width: 100%;
    }}
    .publication-header {{
      margin-bottom: 0.6em;
    }}
    .publication-title {{
      font-size: 1.2em;
      font-weight: bold;
      color: #333;
      margin: 0;
      line-height: 1.3;
    }}
    .publication-links {{
      display: flex;
      gap: 0.5em;
      margin-top: 0.5em;
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
    .doi-link {{
      background: #007cba;
      color: white;
    }}
    .pdf-link {{
      background: #28a745;
      color: white;
    }}
    .code-link {{
      background: #6f42c1;
      color: white;
    }}
    .slides-link {{
      background: #17a2b8;
      color: white;
    }}
    .video-link {{
      background: #dc3545;
      color: white;
    }}
    .publication-meta {{
      margin-bottom: 0.6em;
    }}
    .publication-authors {{
      color: #555;
      font-size: 1em;
      margin-bottom: 0.2em;
      font-weight: 500;
    }}
    .publication-venue {{
      color: #666;
      font-size: 0.9em;
      font-style: italic;
    }}
    .publication-pages {{
      color: #666;
      font-size: 0.85em;
      margin-top: 0.1em;
    }}
    .publication-abstract {{
      color: #555;
      font-size: 0.95em;
      line-height: 1.4;
      font-style: italic;
      margin-top: 0.5em;
    }}
    .section-title {{
      font-size: 1.3em;
      color: #333;
      margin: 1.2em 0 0.6em 0;
      padding-bottom: 0.2em;
      border-bottom: 1px solid #007cba;
      font-weight: 600;
    }}
    .section-title:first-of-type {{
      margin-top: 0;
    }}
    .talk-item {{
      border-left: 3px solid #17a2b8;
      margin: 0.8em 0;
      padding: 0.8em 0 0.8em 0.8em;
      background: none;
      box-sizing: border-box;
      width: 100%;
    }}
    .talk-type {{
      color: #17a2b8;
      font-size: 0.8em;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.3px;
      margin-top: 0.2em;
      display: inline-block;
      background: #e3f2fd;
      padding: 0.2em 0.5em;
      border-radius: 3px;
    }}
    .publication-coauthors {{
      color: #666;
      font-size: 0.85em;
      font-style: italic;
      margin-top: 0.1em;
    }}
    .talk-item .publication-title {{
      font-size: 1.1em;
      margin-bottom: 0.3em;
    }}
    .talk-item .publication-venue {{
      font-size: 0.9em;
      margin-bottom: 0.2em;
    }}
    .talk-item .publication-abstract {{
      font-size: 0.9em;
      margin-top: 0.3em;
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
      position: relative;
    }}
    .nav-link.current {{
      color: #007cba;
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
          <li class="nav-item"><a href="index.html" class="nav-link current">Publications / Talks</a></li>
          <li class="nav-item"><a href="../posts/index.html" class="nav-link">Blog</a></li>
        </ul>
      </nav>
      <button class="nav-toggle" onclick="toggleNav()">☰</button>
    </div>
  </header>

  <div class="hero">
    <div class="container">
      <h1>Publications & Talks</h1>
      <p>Research papers, academic publications, and conference presentations</p>
    </div>
  </div>

  <main class="container">
    <a href="../index.html" class="back-link">← Back to Mainpage</a>
    
    {f'<h2 class="section-title">Publications</h2><ul class="publication-list">{chr(10).join(pub_items)}</ul>' if pub_items else ''}
    {f'<h2 class="section-title">Talks & Presentations</h2><ul class="publication-list">{chr(10).join(talk_items)}</ul>' if talk_items else ''}
  </main>
</body>
</html>"""

def main():
    print("Starting publications generation...")
    
    # Create publications directory if it doesn't exist
    publications_dir = Path("publications")
    publications_dir.mkdir(exist_ok=True)
    
    # Generate publications page
    publications_html = build_publications_page()
    if publications_html:
        (publications_dir / "index.html").write_text(publications_html, encoding="utf-8")
        print("Generated publications/index.html")
    else:
        print("No publications found or error occurred")
        sys.exit(1)
    
    print("Publications generation completed!")

if __name__ == "__main__":
    main()
