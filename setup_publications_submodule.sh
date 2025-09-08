#!/bin/bash
# Setup script to initialize the publications repository as a git submodule

echo "Setting up publications as a git submodule..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "Error: Not in a git repository. Please initialize git first."
    exit 1
fi

# Check if publications directory exists
if [ ! -d "publications" ]; then
    echo "Error: publications directory not found. Please create it first."
    exit 1
fi

# Initialize git in publications directory if not already done
cd publications
if [ ! -d ".git" ]; then
    echo "Initializing git repository in publications..."
    git init
    git add .
    git commit -m "Initial commit: Add publication data and scripts"
    echo "✓ Git repository initialized in publications/"
else
    echo "✓ Git repository already exists in publications/"
fi

cd ..

# Add as submodule (this will be done manually by the user)
echo ""
echo "To complete the setup:"
echo "1. Create a new repository on GitHub for publications"
echo "2. Add the remote origin to the publications directory:"
echo "   cd publications"
echo "   git remote add origin https://github.com/yourusername/publications.git"
echo "   git push -u origin main"
echo "3. Add the submodule to the main repository:"
echo "   git submodule add https://github.com/yourusername/publications.git publications"
echo "4. Commit the submodule addition:"
echo "   git add .gitmodules publications"
echo "   git commit -m 'Add publications as submodule'"
echo ""
echo "After setup, you can update publications with:"
echo "   git submodule update --remote publications"
