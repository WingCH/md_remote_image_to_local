# Core Module Overview

The Core Module contains the main functionality and program entry points for processing remote images in Markdown files. These functions handle command-line arguments, parse Markdown files, and coordinate with image utility and file utility functions.

## Usage

The Core Module provides the main program entry point `main()`, typically called via the command line:

```bash
python md_image_localizer.py /path/to/markdown/files -w 10
```

## Main Features

- Process command-line arguments and configuration
- Search for all Markdown files in the target directory
- Coordinate the processing of images and path updates for each Markdown file
- Provide progress reporting and error handling

## Available Functions

A complete list of functions can be found in the [Core Functions List](./list.md).

### Key Functions:

- [process_directory](./process-directory.md) - Process all Markdown files in a target directory
- [process_markdown_file](./process-markdown-file.md) - Process a single Markdown file, download remote images and update paths
- [main](./main.md) - Program entry point, handling command-line arguments and calling other functions 