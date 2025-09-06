#!/usr/bin/env python3
import os
import re
from pathlib import Path

NOTES_DIR = Path("Notes")
PUBLICATION_DIR = NOTES_DIR / "publication"
BUILD_DIR = Path("build")

def get_publications():
    """Get all publications from Notes/publication directory"""
    publications = []
    
    if not PUBLICATION_DIR.exists():
        return publications
    
    for pdf_file in PUBLICATION_DIR.glob("*.pdf"):
        # Extract publication info from filename
        name = pdf_file.stem
        
        # Try to extract year and title from filename patterns
        # Common patterns: year_title, title_year, etc.
        year_match = re.search(r'(\d{4})', name)
        year = year_match.group(1) if year_match else "Unknown"
        
        # Clean up title - remove year and common patterns
        title = re.sub(r'\d{4}', '', name)
        title = title.replace('_', ' ').replace('-', ' ')
        title = ' '.join(title.split()).title()
        
        # If title is empty or just whitespace, use filename
        if not title.strip():
            title = name.replace('_', ' ').replace('-', ' ').title()
        
        publications.append({
            "title": title,
            "year": year,
            "filename": pdf_file.name,
            "path": f"Notes/publication/{pdf_file.name}"
        })
    
    # Sort by year (newest first), then by title
    publications.sort(key=lambda p: (p["year"], p["title"]), reverse=True)
    return publications

def generate_publications_html():
    """Generate HTML for publications section"""
    publications = get_publications()
    
    if not publications:
        return ""
    
    html = '<section class="publications">\n'
    html += '  <h2>Publications</h2>\n'
    html += '  <ul class="publication-list">\n'
    
    for pub in publications:
        html += f'''    <li class="publication-item">
      <div class="publication-info">
        <h3 class="publication-title">{pub["title"]}</h3>
        <span class="publication-year">({pub["year"]})</span>
      </div>
      <div class="publication-actions">
        <a href="{pub["path"]}" class="pdf-download" target="_blank">📄 PDF</a>
      </div>
    </li>
'''
    
    html += '  </ul>\n'
    html += '</section>\n'
    
    return html

if __name__ == "__main__":
    print(generate_publications_html())
