# Academic Portfolio Build System for PowerShell
# Comprehensive build script for the entire academic portfolio

Write-Host "=== Academic Portfolio Build System ===" -ForegroundColor Cyan
Write-Host "Building complete academic portfolio from TeX and metadata files..." -ForegroundColor White

# Check if we're in the right directory
if (-not (Test-Path "posts")) {
    Write-Host "Error: posts directory not found" -ForegroundColor Red
    Write-Host "Please run this script from the project root directory" -ForegroundColor Red
    exit 1
}

# Clean generated files
Write-Host "`n=== Cleaning Generated Files ===" -ForegroundColor Yellow
Write-Host "Cleaning generated HTML files..." -ForegroundColor White
if (Test-Path "index.html") { Remove-Item "index.html" }
if (Test-Path "posts\index.html") { Remove-Item "posts\index.html" }
if (Test-Path "publications\index.html") { Remove-Item "publications\index.html" }
Write-Host "Cleaning blog post directories..." -ForegroundColor White
Get-ChildItem -Path "posts" -Directory | ForEach-Object {
    if (Test-Path $_.FullName) {
        Remove-Item -Recurse -Force $_.FullName
        Write-Host "✓ Removed $($_.Name)" -ForegroundColor Green
    }
}
Write-Host "✓ Generated files cleaned" -ForegroundColor Green

# Build blog posts from TeX files
Write-Host "`n=== Building Blog Posts ===" -ForegroundColor Yellow
if (Test-Path "build_html.sh") {
    try {
        bash build_html.sh posts/*.tex
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Blog posts built successfully" -ForegroundColor Green
        } else {
            Write-Host "✗ Error building blog posts" -ForegroundColor Red
            exit 1
        }
    } catch {
        Write-Host "✗ Error running build_html.sh: $_" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✗ build_html.sh not found" -ForegroundColor Red
    exit 1
}

# Generate all pages using Python script
Write-Host "`n=== Generating All Pages ===" -ForegroundColor Yellow
try {
    python script/generate_site.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ All pages generated successfully" -ForegroundColor Green
    } else {
        Write-Host "✗ Error generating pages" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "✗ Error running Python script: $_" -ForegroundColor Red
    exit 1
}

# Check required files
Write-Host "`n=== Verifying Required Files ===" -ForegroundColor Yellow
$missing = 0

if (Test-Path "index.html") {
    Write-Host "✓ Main index page exists" -ForegroundColor Green
} else {
    Write-Host "✗ Main index page missing" -ForegroundColor Red
    $missing = 1
}

if (Test-Path "posts\index.html") {
    Write-Host "✓ Blog listing page exists" -ForegroundColor Green
} else {
    Write-Host "✗ Blog listing page missing" -ForegroundColor Red
    $missing = 1
}

if (Test-Path "publications\index.html") {
    Write-Host "✓ Publications page exists" -ForegroundColor Green
} else {
    Write-Host "✗ Publications page missing" -ForegroundColor Red
    $missing = 1
}

# Count blog posts
$postCount = (Get-ChildItem -Path "posts" -Directory | Where-Object { Test-Path "$($_.FullName)\index.html" }).Count
Write-Host "✓ Found $postCount blog post pages" -ForegroundColor Green

# Count PDFs
$pdfCount = (Get-ChildItem -Path "Notes\publication" -Filter "*.pdf" -ErrorAction SilentlyContinue).Count
Write-Host "✓ Found $pdfCount PDF files" -ForegroundColor Green

# Final status
Write-Host ""
if ($missing -eq 0) {
    Write-Host "🎉 Build completed successfully!" -ForegroundColor Green
    Write-Host "All files are ready for deployment." -ForegroundColor White
    Write-Host ""
    Write-Host "To view the site:" -ForegroundColor Cyan
    Write-Host "  - Main page: start index.html" -ForegroundColor White
    Write-Host "  - Blog: start posts\index.html" -ForegroundColor White
    Write-Host "  - Publications: start publications\index.html" -ForegroundColor White
} else {
    Write-Host "❌ Build completed with errors." -ForegroundColor Red
    Write-Host "Some required files are missing." -ForegroundColor Red
    exit 1
}