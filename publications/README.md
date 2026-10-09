# Publications Repository

This repository contains academic publications and research papers metadata.

## Structure

- `data/` - Contains publication metadata files (`.meta.json`)
- `../Notes/publication/` - Contains PDFs and generated preprint landing pages
- `assets/` - Contains any additional assets for publications
- `scripts/` - Contains scripts for generating publication pages

## Usage

This directory holds metadata in the main website repository. PDFs and preprint landing pages live in the existing `Notes/publication` submodule.

## Adding New Publications

1. Initialize `Notes` with `git submodule update --init Notes` and add the PDF to `Notes/publication/`.
2. Create a corresponding `.meta.json` file with publication metadata
3. The main repository's build system will automatically pick up the new publication

Set `"status": "preprint"` to list a paper under Preprints. Set `"pdf"` to its path from the website root, such as `"Notes/publication/your-paper.pdf"`. Abstracts are collapsed behind an Abstract button in the list.

For a preprint landing page, also provide `"landing_page": "Notes/publication/your-paper.html"`, an ISO `"date"`, and the author's full `"abstract"`. Optional fields include `"version"`, `"keywords"`, and `"author_orcids"`. Run `make generate` to build the landing page, publications list, and sitemap. The landing page shows the full abstract and includes Google Scholar citation tags, a canonical URL, JSON-LD, and a BibTeX citation. Its PDF must be in the same directory.

To publish, commit and push the PDF and generated HTML in `Notes`, then commit and push the updated `Notes` pointer and website changes in the main repository. After deployment, submit `https://apiros3.github.io/sitemap.xml` in Google Search Console and request indexing of the landing page. A sitemap helps discovery; indexing is decided by the search engine.

## Metadata Format

Each publication should have a corresponding `.meta.json` file with the following structure:

```json
{
  "title": "Publication Title",
  "authors": ["Author 1", "Author 2"],
  "conference": "Conference Name",
  "year": "2025",
  "abstract": "Abstract text...",
  "venue": "Short Venue Name",
  "code": "https://github.com/username/repo",
  "arxiv": "https://arxiv.org/abs/...",
  "doi": "https://doi.org/..."
}
```
