# Setup script to initialize the publications repository as a git submodule

Write-Host "Setting up publications as a git submodule..." -ForegroundColor Green

# Check if we're in a git repository
if (-not (Test-Path ".git")) {
    Write-Host "Error: Not in a git repository. Please initialize git first." -ForegroundColor Red
    exit 1
}

# Check if publications directory exists
if (-not (Test-Path "publications")) {
    Write-Host "Error: publications directory not found. Please create it first." -ForegroundColor Red
    exit 1
}

# Initialize git in publications directory if not already done
Set-Location publications
if (-not (Test-Path ".git")) {
    Write-Host "Initializing git repository in publications..." -ForegroundColor Yellow
    git init
    git add .
    git commit -m "Initial commit: Add publication data and scripts"
    Write-Host "✓ Git repository initialized in publications/" -ForegroundColor Green
} else {
    Write-Host "✓ Git repository already exists in publications/" -ForegroundColor Green
}

Set-Location ..

Write-Host ""
Write-Host "To complete the setup:" -ForegroundColor Cyan
Write-Host "1. Create a new repository on GitHub for publications" -ForegroundColor White
Write-Host "2. Add the remote origin to the publications directory:" -ForegroundColor White
Write-Host "   cd publications" -ForegroundColor Gray
Write-Host "   git remote add origin https://github.com/yourusername/publications.git" -ForegroundColor Gray
Write-Host "   git push -u origin main" -ForegroundColor Gray
Write-Host "3. Add the submodule to the main repository:" -ForegroundColor White
Write-Host "   git submodule add https://github.com/yourusername/publications.git publications" -ForegroundColor Gray
Write-Host "4. Commit the submodule addition:" -ForegroundColor White
Write-Host "   git add .gitmodules publications" -ForegroundColor Gray
Write-Host "   git commit -m 'Add publications as submodule'" -ForegroundColor Gray
Write-Host ""
Write-Host "After setup, you can update publications with:" -ForegroundColor Cyan
Write-Host "   git submodule update --remote publications" -ForegroundColor Gray
