# Academic Portfolio Build System

A comprehensive build system for generating an academic portfolio website from TeX files and metadata.

## 🚀 Quick Start

### Windows (PowerShell/CMD)
```bash
.\build.bat
```

### Windows (PowerShell)
```powershell
.\build.ps1
```

### Linux/macOS (Make)
```bash
make all
```

## 📁 Project Structure

```
├── index.html                 # Main homepage (GitHub Pages entry point)
├── posts/                     # Blog posts and generated files
│   ├── index.html            # Blog listing page
│   ├── publications.html     # Publications page
│   ├── posts/                # Individual blog posts
│   │   ├── calculus/
│   │   ├── linear-algebra/
│   │   └── ...
│   └── pdf/                  # PDF files
├── posts/                    # TeX source files
│   ├── 2025-01-15-quantum-mechanics.tex
│   ├── 2025-03-10-calculus.tex
│   └── ...
├── Notes/publication/        # Publication metadata
│   └── itp25.meta.json
├── templates/                # HTML templates
├── script/                   # Python generation scripts
├── build_html.sh            # TeX to HTML conversion
├── build.bat                # Windows build script
├── build.ps1                # PowerShell build script
├── Makefile                 # Make-based build system
└── README.md                # This file
```

## 🔧 Build System Components

### 1. TeX to HTML Conversion
- **Script**: `build_html.sh` (TeX to HTML conversion)
- **Input**: TeX files in `posts/` directory
- **Output**: HTML files in `posts/` directory
- **Tool**: Pandoc for conversion

### 2. Blog Listing Generation
- **File**: `posts/index.html`
- **Features**: Tag filtering, clickable articles, abstracts
- **Data Source**: TeX files and metadata

### 3. Publications Page
- **File**: `publications/index.html`
- **Data Source**: `Notes/publication/*.meta.json` files
- **Features**: Rich metadata display, multiple link types

### 4. Main Homepage
- **File**: `index.html`
- **Purpose**: GitHub Pages entry point
- **Features**: Recent articles, contact info, navigation

## 📝 Adding New Content

### Adding a New Blog Post

1. **Create TeX file** in `posts/` directory:
   ```bash
   # Format: YYYY-MM-DD-topic.tex
   posts/2025-12-01-new-topic.tex
   ```

2. **Create metadata file** (optional):
   ```json
   {
     "title": "Your Article Title",
     "date": "2025-12-01",
     "tags": ["mathematics", "analysis"],
     "abstract": "Brief description of the article..."
   }
   ```

3. **Run build system**:
   ```bash
   .\build.bat  # Windows
   make all     # Linux/macOS
   ```

### Adding a New Publication

1. **Create metadata file** in `Notes/publication/`:
   ```json
   {
     "title": "Your Paper Title",
     "authors": ["Author One", "Author Two"],
     "conference": "Conference Name",
     "year": "2025",
     "abstract": "Abstract text...",
     "arxiv": "https://arxiv.org/abs/...",
     "doi": "https://doi.org/...",
     "code": "https://github.com/...",
     "venue": "CONF 2025",
     "pages": "1-10"
   }
   ```

2. **Add PDF file** (optional):
   ```bash
   Notes/publication/your-paper.pdf
   ```

3. **Run build system** to update publications page

## 🛠️ Build System Details

### Windows Build Script (`build.bat`)
- Cleans generated files and directories
- Converts TeX files to HTML using pandoc
- Verifies all required files exist
- Provides detailed status output

### PowerShell Build Script (`build.ps1`)
- Same functionality as batch script
- Better error handling and colored output
- Cross-platform PowerShell support

### Makefile
- Traditional Unix build system
- Multiple targets: `all`, `clean`, `blog`, `main`, `pub`
- Dependency tracking
- Help system

### Python Build System (`build_system.py`)
- Comprehensive build orchestration
- Error handling and verification
- Cross-platform compatibility

## 🔍 Verification

The build system verifies:
- ✅ Main index page exists
- ✅ Blog listing page exists  
- ✅ Publications page exists
- ✅ All blog post pages generated
- ✅ PDF files available

## 🚀 Deployment

### GitHub Pages
1. Push to GitHub repository
2. Enable GitHub Pages in repository settings
3. Set source to "Deploy from a branch"
4. Select main branch and `/ (root)` folder
5. The `index.html` file serves as the entry point

### Local Development
```bash
# View main page
start index.html

# View blog
start posts/index.html

# View publications
start publications/index.html
```

## 📋 Dependencies

- **Pandoc**: TeX to HTML conversion
- **Python**: Build system scripts (optional)
- **Bash**: TeX conversion script (Windows: Git Bash or WSL)

## 🐛 Troubleshooting

### Common Issues

1. **"pandoc not found"**
   - Install pandoc: https://pandoc.org/installing.html
   - Ensure it's in your PATH

2. **"Python not found"**
   - Install Python: https://python.org/downloads/
   - Ensure it's in your PATH

3. **Generated files missing after clean**
   - The build system cleans all generated files
   - If files are missing, they'll be recreated automatically

4. **TeX conversion errors**
   - Check TeX file syntax
   - Ensure all required packages are available
   - Check pandoc version compatibility

### Getting Help

- Check the build output for specific error messages
- Verify all dependencies are installed
- Ensure you're running from the project root directory
- Check file permissions and paths

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the build system
5. Submit a pull request

---

**Happy building! 🎉**