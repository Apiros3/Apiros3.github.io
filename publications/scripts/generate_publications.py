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
    pub_dir = Path("publications/data")
    print(f"Looking for publications in: {pub_dir}")
    
    if pub_dir.exists():
        meta_files = list(pub_dir.glob("*.meta.json"))
        print(f"Found {len(meta_files)} metadata files: {meta_files}")
        
        for meta_file in meta_files:
            print(f"Reading {meta_file}")
            with open(meta_file, "r", encoding="utf-8") as f:
                pub_data = json.load(f)
                publications.append(pub_data)
                print(f"Loaded publication: {pub_data.get('title', 'Untitled')}")
    else:
        print(f"Publication directory does not exist: {pub_dir}")
        return None
    
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
        pdf_filename = meta_file.stem.replace(".meta", "") + ".pdf"
        pdf_path = pub_dir / pdf_filename
        if pdf_path.exists():
            links_html += f'<a href="publications/data/{pdf_filename}" class="pub-link pdf-link" target="_blank">PDF</a>'
        
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
    <a href="../index.html" class="back-link">← Back to Mainpage</a>
    
    <ul class="publication-list">
      {''.join(pub_items)}
    </ul>
  </main>
</body>
</html>"""

def main():
    print("Starting publications generation...")
    
    # Create build directory if it doesn't exist
    build_dir = Path("build")
    build_dir.mkdir(exist_ok=True)
    
    # Generate publications page
    publications_html = build_publications_page()
    if publications_html:
        (build_dir / "publications.html").write_text(publications_html, encoding="utf-8")
        print("Generated build/publications.html")
    else:
        print("No publications found or error occurred")
        sys.exit(1)
    
    print("Publications generation completed!")

if __name__ == "__main__":
    main()
