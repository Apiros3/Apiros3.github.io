"""Generate scholarly landing pages in the existing Notes submodule."""
import json
import posixpath
from datetime import date
from html import escape
from pathlib import Path
from typing import Any, Dict, List
from xml.etree import ElementTree as ET

from .config import NAV_ITEMS, SITE_AUTHOR, SITE_URL
from .template_engine import generate_html_head, generate_navigation, generate_nav_script


def generate_preprint_page(paper: Dict[str, Any]) -> str:
    """Show the author's abstract and citation without requiring JavaScript."""
    page_path = Path(paper["landing_page"])
    base_path = "../" * (len(page_path.parts) - 1)
    page_url = f"{SITE_URL}/{page_path.as_posix()}"
    pdf_url = f"{SITE_URL}/{paper['pdf']}"
    pdf_link = posixpath.relpath(paper["pdf"], page_path.parent.as_posix())
    published = date.fromisoformat(paper["date"])
    display_date = f"{published.day} {published.strftime('%B %Y')}"
    authors = paper["authors"]
    if isinstance(authors, str):
        authors = [authors]
    version = paper.get("version", "")
    version_label = f", version {version}" if version else ""

    citation_tags = [
        ("citation_title", paper["title"]),
        *(("citation_author", author) for author in authors),
        ("citation_publication_date", published.strftime("%Y/%m/%d")),
        ("citation_pdf_url", pdf_url),
    ]
    if paper.get("doi"):
        citation_tags.append(("citation_doi", paper["doi"]))
    citation_head = "".join(
        f'  <meta name="{name}" content="{escape(value, quote=True)}">\n'
        for name, value in citation_tags
    )
    structured_authors = []
    for author in authors:
        person = {"@type": "Person", "name": author}
        if author == SITE_AUTHOR:
            person["url"] = SITE_URL + "/"
        orcid = paper.get("author_orcids", {}).get(author)
        if orcid:
            person["sameAs"] = f"https://orcid.org/{orcid}"
        structured_authors.append(person)
    article = {
        "@context": "https://schema.org",
        "@type": "ScholarlyArticle",
        "@id": page_url,
        "headline": paper["title"],
        "name": paper["title"],
        "author": structured_authors,
        "datePublished": published.isoformat(),
        "abstract": paper["abstract"],
        "description": paper["abstract"],
        "keywords": paper.get("keywords", []),
        "url": page_url,
        "inLanguage": "en",
        "isAccessibleForFree": True,
        "creativeWorkStatus": "Preprint",
        "encoding": {
            "@type": "MediaObject",
            "contentUrl": pdf_url,
            "encodingFormat": "application/pdf",
        },
    }
    if version:
        article["version"] = version
    if paper.get("code"):
        article["isBasedOn"] = {"@type": "SoftwareSourceCode", "codeRepository": paper["code"]}
    # Escaping '<' keeps a title containing '</script>' inside the JSON data.
    json_ld = json.dumps(article, ensure_ascii=False, indent=2).replace("<", "\\u003c")
    extra_head = citation_head + f'  <script type="application/ld+json">\n{json_ld}\n  </script>\n'

    links = f'<a href="{escape(pdf_link, quote=True)}">PDF</a>'
    if paper.get("code"):
        links += f'<a href="{escape(paper["code"], quote=True)}">Code / Lean formalization</a>'
    citation = f"{', '.join(authors)}. {paper['title']}. Preprint{version_label}, {display_date}."
    bibtex = (
        f"@misc{{{page_path.stem},\n"
        f"  author = {{{' and '.join(authors)}}},\n"
        f"  title = {{{paper['title']}}},\n"
        f"  year = {{{published.year}}},\n"
        f"  note = {{Preprint{version_label}, {display_date}}},\n"
        f"  url = {{{page_url}}}\n"
        "}"
    )

    return f"""{generate_html_head(paper['title'], base_path=base_path, description=paper['abstract'], canonical_url=page_url, extra_head=extra_head)}
<body class="paper-page">
{generate_navigation("publications", base_path)}

  <main class="container">
    <article>
      <header class="paper-header">
        <h1 class="citation_title">{escape(paper['title'])}</h1>
        <p class="paper-authors citation_author">{escape(', '.join(authors))}</p>
        <p class="paper-date">Preprint{escape(version_label)} · <time datetime="{published.isoformat()}">{display_date}</time></p>
        <nav class="paper-resources" aria-label="Paper resources">{links}</nav>
      </header>

      <section aria-labelledby="abstract-heading">
        <h2 id="abstract-heading">Abstract</h2>
        <p>{escape(paper['abstract'])}</p>
      </section>

      <section aria-labelledby="citation-heading">
        <h2 id="citation-heading">Citation</h2>
        <p>{escape(citation)}</p>
        <p><a href="{escape(page_url, quote=True)}">{escape(page_url)}</a></p>
        <pre class="paper-citation"><code>{escape(bibtex)}</code></pre>
      </section>
      <p class="paper-back"><a href="{base_path}publications/index.html">All publications and preprints</a></p>
    </article>
  </main>
{generate_nav_script()}
</body>
</html>
"""


def build_preprint_pages(publications: List[Dict[str, Any]]) -> None:
    """Keep paper pages and PDFs together, without creating a new submodule."""
    for paper in publications:
        if paper.get("status") != "preprint":
            continue
        if not Path("Notes/.git").is_file():
            raise RuntimeError("Initialize the PDF submodule first: git submodule update --init Notes")
        page_path = Path(paper["landing_page"])
        pdf_path = Path(paper["pdf"])
        if page_path.parent != Path("Notes/publication") or pdf_path.parent != page_path.parent:
            raise ValueError("Preprint HTML and PDF files must both be in Notes/publication")
        if not pdf_path.is_file():
            raise FileNotFoundError(f"Missing preprint PDF: {pdf_path}")
        if not paper.get("abstract"):
            raise ValueError("Preprints need the author's full abstract in their metadata")
        page_path.write_text(generate_preprint_page(paper), encoding="utf-8")


def generate_sitemap(publications: List[Dict[str, Any]], posts: List[Dict[str, Any]]) -> str:
    """List the site's main pages, blog posts, and canonical paper URLs."""
    paths = [""]
    paths.extend(item["url"].removeprefix("./") for item in NAV_ITEMS if item["url"] not in ("./index.html", "index.html"))
    paths.extend(f"posts/{post['slug']}/index.html" for post in posts)
    paths.extend(paper["landing_page"] for paper in publications if paper.get("landing_page"))
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", namespace)
    root = ET.Element(f"{{{namespace}}}urlset")
    for path in dict.fromkeys(paths):
        entry = ET.SubElement(root, f"{{{namespace}}}url")
        ET.SubElement(entry, f"{{{namespace}}}loc").text = f"{SITE_URL}/{path}"
    ET.indent(root, space="  ")
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="unicode") + "\n"
