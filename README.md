# Markdown Remote Image Localizer

This tool downloads remote images in Markdown files to local storage and updates the image path references in the Markdown.

## Features

- Supports direct dependency installation or running in a virtual environment
- Automatically installs required dependencies from requirements.txt
- Processes all Markdown files in the entire directory
- Identifies and downloads remote images in Markdown
- Saves images to a `resources` directory at the same level as each Markdown file
- Updates image references in Markdown files

## Requirements

- Python 3.6 or higher

## Dependencies

All dependencies are listed in the `requirements.txt` file:
- markdown - for processing Markdown format
- requests - for downloading remote images

## Usage

### Method 1: Direct Dependency Installation (No Virtual Environment)

If you don't want to use a virtual environment, you can directly install the required dependencies and run:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the script
python md_image_localizer.py /path/to/markdown/files
```

### Method 2: Using a Virtual Environment (Recommended)

Using a virtual environment can avoid dependency conflicts, which is the recommended approach:

1. Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate.bat
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the script:

```bash
python md_image_localizer.py /path/to/markdown/files
```

4. After use, you can deactivate the virtual environment:

```bash
deactivate
```

### Example

The `test` directory contains examples showing the before and after state of Markdown files:

```
test/
├── before/
│   └── example.md        # Original Markdown with remote image references
├── after/
│   ├── example.md        # Processed Markdown with local image references
│   └── resources/        # Downloaded images stored here
│       ├── GitHub-Mark.png
│       ├── icon256.png
│       └── 1200px-Python-logo-notext.svg.png
└── local-image.png       # Example local image (not modified by the tool)
```

To run the tool on your own Markdown files:

```bash
# Whether using a virtual environment or not
python md_image_localizer.py ./path/to/your/markdown/files
```

## How It Works

1. Search for all Markdown (`.md`) files in the specified directory
2. Parse each Markdown file, identifying remote image URLs
3. Create a `resources` subdirectory for each Markdown file's directory
4. Download images to the appropriate `resources` directory
5. Update image references in the Markdown file with relative paths

## Supported Image Reference Formats

- Standard Markdown format: `![alt text](http://example.com/image.jpg)`
- HTML tag format: `<img src="http://example.com/image.jpg" alt="alt text" />` 