@echo off
REM Academic Portfolio Build System for Windows
REM Comprehensive build script for the entire academic portfolio

setlocal enabledelayedexpansion

echo === Academic Portfolio Build System ===
echo Building complete academic portfolio from TeX and metadata files...

REM Check if we're in the right directory
if not exist "posts" (
    echo Error: posts directory not found
    echo Please run this script from the project root directory
    exit /b 1
)

REM Clean generated files
echo.
echo === Cleaning Generated Files ===
echo Cleaning generated HTML files...
if exist "index.html" del "index.html"
if exist "posts\index.html" del "posts\index.html"
if exist "publications\index.html" del "publications\index.html"
echo Cleaning blog post directories...
for /d %%d in (posts\*) do (
    if exist "%%d" (
        rmdir /s /q "%%d"
        echo ✓ Removed %%d
    )
)
echo ✓ Generated files cleaned

REM Build blog posts from TeX files
echo.
echo === Building Blog Posts ===
if exist "build_html.sh" (
    bash build_html.sh posts/*.tex
    if !errorlevel! equ 0 (
        echo ✓ Blog posts built successfully
    ) else (
        echo ✗ Error building blog posts
        exit /b 1
    )
) else (
    echo ✗ build_html.sh not found
    exit /b 1
)

REM Generate all pages using Python script
echo.
echo === Generating All Pages ===
python script/generate_site.py
if !errorlevel! equ 0 (
    echo ✓ All pages generated successfully
) else (
    echo ✗ Error generating pages
    exit /b 1
)

REM Check required files
echo.
echo === Verifying Required Files ===
set missing=0

if exist "index.html" (
    echo ✓ Main index page exists
) else (
    echo ✗ Main index page missing
    set missing=1
)

if exist "posts\index.html" (
    echo ✓ Blog listing page exists
) else (
    echo ✗ Blog listing page missing
    set missing=1
)

if exist "publications\index.html" (
    echo ✓ Publications page exists
) else (
    echo ✗ Publications page missing
    set missing=1
)

REM Count blog posts
set post_count=0
for /d %%d in (posts\*) do (
    if exist "%%d\index.html" (
        set /a post_count+=1
    )
)
echo ✓ Found !post_count! blog post pages

REM Count PDFs
set pdf_count=0
for %%f in (Notes\publication\*.pdf) do (
    set /a pdf_count+=1
)
echo ✓ Found !pdf_count! PDF files

REM Final status
echo.
if !missing! equ 0 (
    echo 🎉 Build completed successfully!
    echo All files are ready for deployment.
    echo.
    echo To view the site:
    echo   - Main page: start index.html
    echo   - Blog: start posts\index.html
    echo   - Publications: start publications\index.html
) else (
    echo ❌ Build completed with errors.
    echo Some required files are missing.
    exit /b 1
)

endlocal