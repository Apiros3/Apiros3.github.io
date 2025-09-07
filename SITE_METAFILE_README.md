# Site Metafile System

This system allows you to easily configure your root `index.html` page by editing a simple JSON metafile instead of modifying the Python code directly.

## Files

- `site.meta.json` - The main configuration file for your site
- `script/config.py` - Loads and processes the metafile data
- `script/page_generators.py` - Uses the metafile data to generate pages
- `script/generate_site_new.py` - Main site generation script

## Configuration Options

The `site.meta.json` file contains the following sections:

### Site Information
```json
{
  "site": {
    "title": "Apiros3",
    "description": "Academic Portfolio", 
    "author": "Apiros3"
  }
}
```

### About Section
```json
{
  "about": {
    "title": "About Me",
    "content": "Your about section content here..."
  }
}
```

### Contact Information
```json
{
  "contact": {
    "email": "your.email@institution.edu",
    "institution": "[Your Institution]",
    "department": "Mathematics & Computer Science",
    "location": "[Your Location]"
  }
}
```

### Navigation
```json
{
  "navigation": {
    "brand": "Apiros3",
    "items": [
      {
        "name": "About",
        "url": "./index.html",
        "current": true
      },
      {
        "name": "Publications", 
        "url": "publications/index.html",
        "current": false
      },
      {
        "name": "Blog",
        "url": "posts/index.html", 
        "current": false
      }
    ]
  }
}
```

### Recent Posts Section
```json
{
  "recent_posts": {
    "title": "Recent Blog Posts",
    "limit": 5,
    "show_abstract": false,
    "show_tags": false
  }
}
```

## How to Use

1. **Edit the metafile**: Modify `site.meta.json` with your desired content
2. **Regenerate the site**: Run the site generation script
   ```bash
   # In WSL (recommended)
   wsl python3 script/generate_site_new.py
   
   # Or in PowerShell
   python script/generate_site_new.py
   ```
3. **View changes**: The `index.html` file will be automatically updated with your changes

## Example: Updating Your About Section

1. Open `site.meta.json`
2. Modify the `about` section:
   ```json
   {
     "about": {
       "title": "About Dr. Smith",
       "content": "I am a professor of Computer Science at XYZ University, specializing in machine learning and artificial intelligence. My research focuses on developing novel algorithms for natural language processing and computer vision applications."
     }
   }
   ```
3. Run the generation script
4. Your `index.html` will now show the updated about section

## Example: Updating Contact Information

1. Edit the `contact` section in `site.meta.json`:
   ```json
   {
     "contact": {
       "email": "john.smith@university.edu",
       "institution": "XYZ University",
       "department": "Computer Science",
       "location": "Boston, MA"
     }
   }
   ```
2. Regenerate the site
3. The contact information in the footer will be updated

## Example: Changing Navigation

1. Modify the `navigation` section:
   ```json
   {
     "navigation": {
       "brand": "Dr. Smith's Lab",
       "items": [
         {
           "name": "Home",
           "url": "./index.html",
           "current": true
         },
         {
           "name": "Research",
           "url": "research/index.html",
           "current": false
         },
         {
           "name": "Publications",
           "url": "publications/index.html",
           "current": false
         },
         {
           "name": "Blog",
           "url": "posts/index.html",
           "current": false
         }
       ]
     }
   }
   ```
2. Regenerate the site
3. The navigation will be updated with your new brand name and menu items

## Fallback Behavior

If the `site.meta.json` file is missing or corrupted, the system will automatically fall back to default values defined in `script/config.py`. This ensures your site will always generate successfully.

## Tips

- Always validate your JSON syntax before regenerating
- Make a backup of your `site.meta.json` before making major changes
- The system automatically handles URL path adjustments for different page contexts
- Changes to the metafile take effect immediately after regeneration
