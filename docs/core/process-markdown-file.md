# process_markdown_file

Process a single Markdown file, download remote images contained within it, and update the reference paths.

## Function Signature

```python
def process_markdown_file(file_path, target_dir, max_workers=10):
    """
    Process a single Markdown file, download remote images and update paths
    
    Returns:
        tuple: (images_found, images_updated) - Number of images found and successfully updated
    """
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `file_path` | `str` | Required | Path to the Markdown file |
| `target_dir` | `str` | Required | Target directory being processed |
| `max_workers` | `int` | `10` | Maximum number of parallel download threads |

## Return Value

Returns a tuple `(images_found, images_updated)`:
- `images_found`: `int` - Number of remote images found in the Markdown file
- `images_updated`: `int` - Number of images successfully downloaded and updated in the Markdown file

## Detailed Description

This function is the core processor for individual Markdown files, executing the following steps:

1. Read the Markdown file content
2. Use the `extract_image_urls` function to find remote image URLs in the content
3. Create a `resources` subdirectory in the same directory as the Markdown file
4. Use the `batch_download_images` function to download all remote images in parallel
5. Update image references in the Markdown file (changing remote URLs to local relative paths)
6. Save the modified Markdown file
7. Return the count of images found and successfully updated

## Error Handling

The function includes the following error handling mechanisms:
- Attempts to read files with different encodings (utf-8 and big5)
- Catches and logs errors during file reading and writing operations
- Uses tqdm.write instead of print to avoid interfering with progress bar display

## Example

```python
# Process a single Markdown file
images_found, images_updated = process_markdown_file('./README.md', './', max_workers=10)
print(f"Found {images_found} images, updated {images_updated} image references")
```

## Related Functions

- [extract_image_urls](../image-utils/extract-image-urls.md) - Extract image URLs from Markdown content
- [batch_download_images](../image-utils/batch-download-images.md) - Download images in batch
- [process_directory](./process-directory.md) - Process all Markdown files in a directory 