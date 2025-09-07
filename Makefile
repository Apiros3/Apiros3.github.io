# Academic Portfolio Build System
# Comprehensive Makefile for building the entire academic portfolio
# 
# Usage:
#   make all        - Build everything
#   make clean      - Clean all build files
#   make blog       - Build blog posts only
#   make main       - Build main index only
#   make pub        - Build publications only
#   make verify     - Verify all files exist
#   make help       - Show this help

.PHONY: all clean create-files blog generate main pub blog-list verify help install test

# Default target
all: clean create-files blog generate verify

# Build main index page (alias for generate)
main: generate

# Build blog posts from TeX files
blog:
	@echo "Building blog posts from TeX files..."
	@bash build_html.sh posts/*.tex
	@echo "✓ Blog posts built"

# Build all pages using unified generation script
# Generate PDFs from TeX files
pdf:
	@echo "Generating PDFs from TeX files..."
	@for tex_file in posts/*.tex; do \
		if [ -f "$$tex_file" ]; then \
			echo "Compiling $$tex_file..."; \
			base=$$(basename "$$tex_file" .tex); \
			date=$$(echo "$$base" | cut -d- -f1-3); \
			slug=$$(echo "$$base" | cut -d- -f4-); \
			if [ -n "$$slug" ]; then \
				cd posts && pdflatex -interaction=nonstopmode "$$(basename "$$tex_file")" && cd ..; \
				mkdir -p "posts/$$slug"; \
				mv "posts/$$base.pdf" "posts/$$slug/$$slug.pdf"; \
				echo "✓ Moved PDF to posts/$$slug/$$slug.pdf"; \
			fi; \
		fi; \
	done
	@echo "✓ PDFs generated and organized"

# Generate all pages
generate:
	@echo "Generating all pages..."
	@python3 script/generate_site.py
	@echo "✓ All pages generated"

# Build blog listing page (alias for generate)
blog-list: generate

# Build publications page (alias for generate)
pub: generate

# Verify all required files exist
verify:
	@echo "Verifying build..."
	@echo "Checking required files:"
	@for file in index.html blog.html publications.html; do \
		if [ -f "$$file" ]; then \
			echo "✓ $$file"; \
		else \
			echo "✗ $$file MISSING"; \
		fi; \
	done
	@echo "Checking blog posts:"
	@if [ -d "posts" ]; then \
		post_count=$$(find posts -name "index.html" | wc -l); \
		echo "✓ Found $$post_count blog post pages in posts/"; \
	else \
		echo "✗ No blog posts directory"; \
	fi
	@echo "Checking PDFs:"
	@if [ -d "Notes/publication" ]; then \
		pdf_count=$$(find Notes/publication -name "*.pdf" | wc -l); \
		echo "✓ Found $$pdf_count PDF files"; \
	else \
		echo "✗ No PDF directory"; \
	fi

# Clean build files (preserve important files)
clean:
	@echo "Cleaning build files..."
	@if [ -d "build" ]; then \
		rm -rf build/pdf; \
		mkdir -p build/pdf; \
	fi
	@echo "✓ Build files cleaned"

# Create/update files
create-files:
	@echo "Creating/updating files..."
	@chmod +x create_missing_files.sh
	@./create_missing_files.sh

# Install dependencies (if needed)
install:
	@echo "Installing dependencies..."
	@if command -v pandoc >/dev/null 2>&1; then \
		echo "✓ pandoc is installed"; \
	else \
		echo "✗ pandoc not found - please install pandoc"; \
		exit 1; \
	fi
	@if command -v python >/dev/null 2>&1; then \
		echo "✓ python is available"; \
	else \
		echo "✗ python not found - please install python"; \
		exit 1; \
	fi

# Test the build system
test: clean blog generate verify
	@echo "✓ All tests passed!"

# Show help
help:
	@echo "Academic Portfolio Build System"
	@echo ""
	@echo "Available targets:"
	@echo "  all        - Build everything (default)"
	@echo "  clean      - Clean all build files"
	@echo "  blog       - Build blog posts from TeX files"
	@echo "  generate   - Generate all HTML pages"
	@echo "  main       - Generate main index page"
	@echo "  pub        - Generate publications page"
	@echo "  blog-list  - Generate blog listing page"
	@echo "  verify     - Verify all files exist"
	@echo "  install    - Check dependencies"
	@echo "  test       - Run full test build"
	@echo "  help       - Show this help message"
	@echo ""
	@echo "The build system works as follows:"
	@echo "1. TeX files in posts/ are converted to HTML using pandoc"
	@echo "2. Blog listing page shows all posts with filtering"
	@echo "3. Publications page shows research papers"
	@echo "4. Main index page serves as the homepage"
	@echo ""
	@echo "Blog posts are used directly from posts/ directory"
	@echo "Other HTML files are generated in the build/ directory"
	@echo "except for index.html which is in the root for GitHub Pages"