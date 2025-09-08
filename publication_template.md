# Publication Metadata Template

This document shows how to create publication metadata files for the academic portfolio.

## File Structure

Create a `.meta.json` file for each publication in the `Notes/publication/` directory.

## Metadata Fields

### Required Fields
- `title`: Publication title
- `authors`: Array of author names
- `conference`: Conference/journal name
- `year`: Publication year
- `abstract`: Brief description of the work

### Optional Fields
- `arxiv`: arXiv link (if available)
- `doi`: DOI link (if available)
- `code`: Code repository link (if available)
- `venue`: Specific venue details
- `pages`: Page numbers
- `volume`: Volume number
- `issue`: Issue number

## Example Files

### Example 1: Conference Paper
```json
{
  "title": "A Novel Approach to Quantum Computing",
  "authors": ["John Smith", "Jane Doe", "Your Name"],
  "conference": "International Conference on Quantum Computing",
  "year": "2024",
  "abstract": "We present a novel approach to quantum computing that improves upon existing methods by 40%. Our technique combines machine learning with quantum algorithms to achieve unprecedented performance in optimization problems.",
  "arxiv": "https://arxiv.org/abs/2401.12345",
  "code": "https://github.com/username/repository",
  "venue": "ICQC 2024",
  "pages": "123-135"
}
```

### Example 2: Journal Article
```json
{
  "title": "Mathematical Foundations of Machine Learning",
  "authors": ["Your Name", "Alice Johnson"],
  "conference": "Journal of Machine Learning Research",
  "year": "2023",
  "abstract": "This paper establishes rigorous mathematical foundations for modern machine learning algorithms, providing theoretical guarantees for convergence and generalization.",
  "doi": "https://doi.org/10.1234/jmlr.2023.001",
  "venue": "JMLR",
  "volume": "24",
  "issue": "1",
  "pages": "1-45"
}
```

### Example 3: Workshop Paper
```json
{
  "title": "Preliminary Results on Neural Architecture Search",
  "authors": ["Your Name"],
  "conference": "Workshop on Neural Architecture Search",
  "year": "2023",
  "abstract": "We present preliminary results on automated neural architecture search, showing promising improvements in efficiency and accuracy.",
  "venue": "NAS Workshop @ ICML 2023"
}
```

## File Naming Convention

- Use descriptive names: `quantum-computing-2024.meta.json`
- Include year for easy sorting
- Use hyphens instead of spaces
- Keep names concise but descriptive

## How to Use

1. Create a `.meta.json` file in `Notes/publication/`
2. Fill in the metadata using the template above
3. Run the portfolio generation script
4. The publication will appear on the publications page

## Notes

- The `abstract` field is displayed prominently on the publications page
- Authors are displayed in the order listed
- Conference/journal names are shown with year
- Optional links (arXiv, DOI) appear as clickable buttons
- All fields support basic HTML formatting if needed
