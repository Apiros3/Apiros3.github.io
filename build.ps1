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

# Clean build directory
Write-Host "`n=== Cleaning Build Directory ===" -ForegroundColor Yellow
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
}
New-Item -ItemType Directory -Path "build\posts" -Force | Out-Null
New-Item -ItemType Directory -Path "build\pdf" -Force | Out-Null
Write-Host "✓ Build directory cleaned" -ForegroundColor Green

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

# Check required files
Write-Host "`n=== Verifying Required Files ===" -ForegroundColor Yellow
$missing = 0

if (Test-Path "index.html") {
    Write-Host "✓ Main index page exists" -ForegroundColor Green
} else {
    Write-Host "✗ Main index page missing" -ForegroundColor Red
    $missing = 1
}

if (Test-Path "build\index.html") {
    Write-Host "✓ Blog listing page exists" -ForegroundColor Green
} else {
    Write-Host "✗ Blog listing page missing" -ForegroundColor Red
    $missing = 1
}

if (Test-Path "build\publications.html") {
    Write-Host "✓ Publications page exists" -ForegroundColor Green
} else {
    Write-Host "✗ Publications page missing" -ForegroundColor Red
    $missing = 1
}

# Count blog posts
$postCount = (Get-ChildItem -Path "build\posts" -Directory | Where-Object { Test-Path "$($_.FullName)\index.html" }).Count
Write-Host "✓ Found $postCount blog post pages" -ForegroundColor Green

# Count PDFs
$pdfCount = (Get-ChildItem -Path "build\pdf" -Filter "*.pdf").Count
Write-Host "✓ Found $pdfCount PDF files" -ForegroundColor Green

# Final status
Write-Host ""
if ($missing -eq 0) {
    Write-Host "🎉 Build completed successfully!" -ForegroundColor Green
    Write-Host "All files are ready for deployment." -ForegroundColor White
    Write-Host ""
    Write-Host "To view the site:" -ForegroundColor Cyan
    Write-Host "  - Main page: start index.html" -ForegroundColor White
    Write-Host "  - Blog: start build\index.html" -ForegroundColor White
    Write-Host "  - Publications: start build\publications.html" -ForegroundColor White
} else {
    Write-Host "❌ Build completed with errors." -ForegroundColor Red
    Write-Host "Some required files are missing." -ForegroundColor Red
    exit 1
}