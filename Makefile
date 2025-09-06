SHELL := /usr/bin/env bash

# Only include properly dated posts (ignore template.tex)
POSTS := $(shell find posts -maxdepth 1 -type f -name '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-*.tex' | sort)

BUILD_DIR  := build
POSTS_DIR  := $(BUILD_DIR)/posts
PDF_DIR    := $(BUILD_DIR)/pdf

.PHONY: all html pdf markdown assets index clean serve new doctor

all: html pdf markdown assets index

html:
	@echo "==> Building HTML from LaTeX with Pandoc + KaTeX"
	@mkdir -p "$(POSTS_DIR)"
	@./build_html.sh $(POSTS)

markdown:
	@echo "==> Building Markdown from LaTeX files"
	@mkdir -p "$(POSTS_DIR)"
	@for f in $(POSTS); do \
		name=$$(basename $$f); \
		base=$${name%.tex}; \
		slug=$$(echo $$base | cut -d- -f4-); \
		if [ -n "$$slug" ]; then \
			outdir="$(POSTS_DIR)/$$slug"; \
			mkdir -p "$$outdir"; \
			echo "Converting $$f to Markdown..."; \
			pandoc "$$f" -t markdown -o "$$outdir/content.md"; \
		fi; \
	done

pdf:
	@echo "==> Building PDFs with Tectonic"
	@mkdir -p "$(PDF_DIR)"
	@for f in $(POSTS); do \
		name=$$(basename "$$f"); \
		base=$${name%.tex}; \
		slug=$$(echo $$base | cut -d- -f4-); \
		tectonic "posts/$$base.tex" --outdir "$(PDF_DIR)"; \
		if [ -f "$(PDF_DIR)/$$base.pdf" ]; then \
			mv "$(PDF_DIR)/$$base.pdf" "$(PDF_DIR)/$$slug.pdf"; \
		fi; \
	done

assets:
	@echo "==> Copying assets"
	@if [[ -d assets ]]; then rsync -a assets/ $(BUILD_DIR)/assets/; else echo "(no assets/ dir)"; fi

index:
	@echo "==> Generating academic homepage as index.html"
	@python3 script/generate_academic_homepage.py
	@echo "==> Adding navigation between posts"
	@python3 script/generate_navigation.py

serve:
	@echo "==> Serving build/ at http://localhost:8080"
	@python3 -m http.server 8080 --directory $(BUILD_DIR)

clean:
	rm -rf $(BUILD_DIR)

# Create a new post from the LaTeX template.
# Usage: make new SLUG=my-new-post DATE=2025-09-06
DATE ?= $(shell date +%Y-%m-%d)
new:
	@if [[ -z "$(SLUG)" ]]; then echo "Usage: make new SLUG=my-post [DATE=YYYY-MM-DD]"; exit 1; fi
	cp posts/template.tex posts/$(DATE)-$(SLUG).tex
	@echo '{ "title": "'$(shell echo $(SLUG) | sed -E 's/-/ /g;s/\b(.)/\U\1/g')'", "tags": [] }' > posts/$(SLUG).meta.json

doctor:
	@echo "==> Environment check"
	@command -v pandoc   >/dev/null || echo "Missing: pandoc"
	@command -v tectonic >/dev/null || echo "Missing: tectonic"
	@command -v jq       >/dev/null || echo "Missing: jq (optional)"
	@printf 'Makefile line endings: '; (file Makefile | grep -q CRLF && echo CRLF || echo LF)
