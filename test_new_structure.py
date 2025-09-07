#!/usr/bin/env python3
"""
Test script to verify the new organized structure works correctly.
"""
import sys
from pathlib import Path

# Add script directory to path
sys.path.insert(0, str(Path(__file__).parent / "script"))

def test_imports():
    """Test that all modules can be imported."""
    try:
        from script.config import SITE_TITLE, CSS_FILES
        from script.data_loader import get_all_posts, get_publications
        from script.template_engine import generate_html_head, generate_navigation
        from script.page_generators import generate_main_index
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_css_files():
    """Test that all CSS files exist."""
    css_files = [
        "css/main.css",
        "css/base.css", 
        "css/layout.css",
        "css/components.css",
        "css/markdown.css"
    ]
    
    missing_files = []
    for css_file in css_files:
        if not Path(css_file).exists():
            missing_files.append(css_file)
    
    if missing_files:
        print(f"❌ Missing CSS files: {missing_files}")
        return False
    else:
        print("✅ All CSS files exist")
        return True

def test_config():
    """Test configuration loading."""
    try:
        from script.config import SITE_TITLE, CSS_FILES, NAV_ITEMS
        print(f"✅ Config loaded: {SITE_TITLE}")
        print(f"   CSS files: {len(CSS_FILES)}")
        print(f"   Nav items: {len(NAV_ITEMS)}")
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_template_generation():
    """Test basic template generation."""
    try:
        from script.template_engine import generate_html_head, generate_navigation
        
        # Test HTML head generation
        head = generate_html_head("Test Page")
        if "<title>Test Page</title>" in head:
            print("✅ HTML head generation works")
        else:
            print("❌ HTML head generation failed")
            return False
        
        # Test navigation generation
        nav = generate_navigation("about")
        if "site-header" in nav and "nav-list" in nav:
            print("✅ Navigation generation works")
        else:
            print("❌ Navigation generation failed")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Template generation error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing new organized structure...")
    print()
    
    tests = [
        ("CSS Files", test_css_files),
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Template Generation", test_template_generation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        if test_func():
            passed += 1
        print()
    
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! New structure is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
