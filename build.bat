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

REM Clean build directory (but preserve important files)
echo.
echo === Cleaning Build Directory ===
if exist "build" (
    REM Backup important files
    if exist "build\index.html" copy "build\index.html" "build\index.html.backup" >nul
    if exist "build\publications.html" copy "build\publications.html" "build\publications.html.backup" >nul
    
    REM Clean posts and pdf directories
    if exist "build\posts" rmdir /s /q build\posts
    if exist "build\pdf" rmdir /s /q build\pdf
    mkdir build\posts
    mkdir build\pdf
    
    REM Restore important files
    if exist "build\index.html.backup" (
        move "build\index.html.backup" "build\index.html" >nul
    )
    if exist "build\publications.html.backup" (
        move "build\publications.html.backup" "build\publications.html" >nul
    )
) else (
    mkdir build\posts
    mkdir build\pdf
)
echo ✓ Build directory cleaned

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

if exist "build\index.html" (
    echo ✓ Blog listing page exists
) else (
    echo ✗ Blog listing page missing
    set missing=1
)

if exist "build\publications.html" (
    echo ✓ Publications page exists
) else (
    echo ✗ Publications page missing
    set missing=1
)

REM Count blog posts
set post_count=0
for /d %%d in (build\posts\*) do (
    if exist "%%d\index.html" (
        set /a post_count+=1
    )
)
echo ✓ Found !post_count! blog post pages

REM Count PDFs
set pdf_count=0
for %%f in (build\pdf\*.pdf) do (
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
    echo   - Blog: start build\index.html
    echo   - Publications: start build\publications.html
) else (
    echo ❌ Build completed with errors.
    echo Some required files are missing.
    exit /b 1
)

endlocal