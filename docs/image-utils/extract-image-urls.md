# extract_image_urls

Extract all remote image URLs from Markdown content.

## Function Signature

```python
def extract_image_urls(markdown_content):
    """
    Extract image URLs from Markdown content
    
    Args:
        markdown_content: The Markdown content string to process
        
    Returns:
        list: A list of image URLs extracted from the Markdown content
    """
```

## Parameters

| Name | Type | Description |
|------|------|-------------|
| `markdown_content` | `str` | The Markdown content string to process |

## Return Value

Returns a `list` containing all image URLs extracted from the Markdown content.

## Detailed Description

This function is responsible for parsing Markdown content and extracting all remote image URLs. It supports two formats of image references:

1. Standard Markdown format: `![alt text](http://example.com/image.jpg)`
2. HTML tag format: `<img src="http://example.com/image.jpg" alt="alt text" />`

The function uses regular expression patterns to match these formats and performs the following processing:

1. Uses `standard_pattern` to match standard Markdown format image references
2. Uses `html_pattern` to match HTML tag format image references
3. Validates each URL found:
   - Checks if it's a valid URL (using the `is_url` function)
   - Checks if it's an image URL (using the `is_image_url` function)
4. Returns a list of all valid image URLs

## Example

```python
# Extract image URLs from a Markdown string
markdown_content = """
# Example Document

This is a Markdown file with images.

![Example Image](https://example.com/image.png)

<img src="https://example.com/another-image.jpg" alt="Another Image" />
"""

image_urls = extract_image_urls(markdown_content)
print(image_urls)
# Output: ['https://example.com/image.png', 'https://example.com/another-image.jpg']
```

## Related Functions

- [is_url](./is-url.md) - Check if a string is a URL
- [is_image_url](./is-image-url.md) - Check if a URL points to an image 