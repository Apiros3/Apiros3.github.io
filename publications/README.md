# Publications Repository

This repository contains academic publications and research papers metadata.

## Structure

- `data/` - Contains publication metadata files (`.meta.json`) and PDFs
- `assets/` - Contains any additional assets for publications
- `scripts/` - Contains scripts for generating publication pages

## Usage

This repository is designed to be used as a submodule in the main academic portfolio repository. The main repository will reference the publication data from this separate repository.

## Adding New Publications

1. Add the publication PDF to `data/`
2. Create a corresponding `.meta.json` file with publication metadata
3. The main repository's build system will automatically pick up the new publication

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
