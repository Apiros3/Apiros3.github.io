#!/bin/bash
# Script to create missing files

echo "Creating missing files..."

# Create necessary directories if they don't exist
# Only create posts directory if it doesn't exist and we have TeX files
if [ ! -d "posts" ] && [ -n "$(find . -maxdepth 1 -name '*.tex' -type f)" ]; then
    mkdir -p posts
fi
mkdir -p publications
mkdir -p Notes/publication

# Publications page is now generated dynamically by the build system
# No need to create a hardcoded template

echo "✓ Files created/updated"