# Markdown Remote Image Localizer

This utility library provides a set of functions for downloading remote images in Markdown files to local storage and updating image reference paths in the Markdown files.

## Feature Overview

- Identifies and downloads remote images in Markdown files
- Automatically creates a `resources` directory to store downloaded images
- Updates image reference paths in Markdown files
- Supports parallel downloads for improved performance
- Provides progress bars to track the overall process

## Modules

This library is divided into the following main modules:

- [Core Module](./core/overview.md) - Provides the main functionality and program entry points
- [Image Utilities](./image-utils/overview.md) - Handles image URL identification and download
- [File Utilities](./file-utils/overview.md) - Handles file reading, writing, and path processing

## Quick Start

For detailed usage instructions, refer to the [Core Module Overview](./core/overview.md) and [README.md](../README.md).

```python
# Basic usage
python md_image_localizer.py /path/to/markdown/files

# Specify number of parallel download threads
python md_image_localizer.py /path/to/markdown/files -w 15
```

## Requirements

- Python 3.6 or higher
- Dependencies: markdown, requests, tqdm (see requirements.txt) 