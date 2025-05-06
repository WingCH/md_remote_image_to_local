# Image Utilities Module Overview

The Image Utilities Module provides functionality related to image URL identification, validation, and downloading. These functions are responsible for extracting image URLs from Markdown content, verifying if URLs point to images, downloading images, and more.

## Main Features

- Identification and validation of image URLs
- Extraction of image URLs from Markdown content
- Downloading individual images and batch downloading multiple images
- Providing parallel download capabilities for improved performance

## Available Functions

A complete list of functions can be found in the [Image Utilities Functions List](./list.md).

### Key Functions:

- [is_url](./is-url.md) - Check if a string is a URL
- [is_image_url](./is-image-url.md) - Check if a URL points to an image
- [extract_image_urls](./extract-image-urls.md) - Extract image URLs from Markdown content
- [download_image](./download-image.md) - Download a single image
- [batch_download_images](./batch-download-images.md) - Download multiple images in parallel

## Usage Example

```python
# Extract image URLs
markdown_content = "![Example Image](https://example.com/image.png)"
image_urls = extract_image_urls(markdown_content)

# Download images
if image_urls:
    url_to_path_map = batch_download_images(image_urls, "./resources", max_workers=5)
    print(f"Downloaded {len(url_to_path_map)} images")
``` 