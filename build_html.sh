#!/bin/bash
set -euo pipefail

for f in "$@"; do
    echo "$f"
    name=$(basename "$f")
    base=${name%.tex}
    date=$(echo "$base" | cut -d- -f1-3)
    slug=$(echo "$base" | cut -d- -f4-)
    
    if [ -z "$slug" ]; then
        echo "Skip $f (bad name)"
        continue
    fi
    
    outdir="posts/$slug"
    mkdir -p "$outdir"
    
    meta_json="posts/${slug}.meta.json"
    TAGS='[]'
    if [ -f "$meta_json" ] && command -v jq >/dev/null 2>&1; then
        TAGS=$(jq -c '.tags // []' "$meta_json" || echo '[]')
    fi
    
    # Keep tags as JSON for template processing
    TAG_ARGS="--metadata=tags_json:$TAGS"
    
    # Get abstract from meta file
    ABSTRACT_FILE="$outdir/abstract.txt"
    ABSTRACT_ARGS=""
    if [ -f "$meta_json" ] && command -v jq >/dev/null 2>&1; then
        ABSTRACT=$(jq -r '.abstract // ""' "$meta_json" || echo "")
        if [ -n "$ABSTRACT" ]; then
            echo "$ABSTRACT" > "$ABSTRACT_FILE"
            ABSTRACT_ARGS="--metadata-file=$ABSTRACT_FILE"
        fi
    fi
    
    echo "Running pandoc for $base.tex..."
    
    # Generate Markdown version
    pandoc "posts/$base.tex" -t markdown \
        --metadata=title:"$(echo $slug | sed 's/-/ /g' | sed 's/\b\w/\U&/g')" \
        --metadata=date:"$date" \
        $TAG_ARGS \
        $ABSTRACT_ARGS \
        --resource-path=.:posts \
        -o "$outdir/content.md"
    
    # Generate PDF from TeX file
    echo "Generating PDF for $base.tex..."
    cd posts && pdflatex -interaction=nonstopmode "$base.tex" && cd ..
    if [ -f "posts/$base.pdf" ]; then
        mv "posts/$base.pdf" "$outdir/$slug.pdf"
        echo "✓ PDF generated: $outdir/$slug.pdf"
    fi
    
    # Generate HTML from Markdown (this becomes the main index.html)
    pandoc "$outdir/content.md" -s -t html5 --katex \
        --template=templates/markdown_post.html \
        --metadata=pdf_url:"$slug.pdf" \
        --metadata=title:"$(echo $slug | sed 's/-/ /g' | sed 's/\b\w/\U&/g')" \
        --metadata=date:"$date" \
        $TAG_ARGS \
        $ABSTRACT_ARGS \
        -o "$outdir/index.html"
    
    # Add JavaScript for KaTeX rendering
    sed -i 's|</head>|  <script>\n    window.addEventListener("load", function() {\n      // Render math elements that already have the math class\n      const mathElements = document.querySelectorAll(".math");\n      mathElements.forEach(function(element) {\n        const isDisplay = element.classList.contains("display");\n        try {\n          katex.render(element.textContent, element, {\n            displayMode: isDisplay,\n            throwOnError: false\n          });\n        } catch (e) {\n          console.error("KaTeX rendering error:", e);\n        }\n      });\n    });\n  </script>\n</head>|' "$outdir/index.html"
    
    echo "Pandoc completed for $base.tex (Markdown generated)"
done
