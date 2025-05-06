# read_markdown_file

Read a Markdown file with automatic encoding detection.

## Function Signature

```python
def read_markdown_file(file_path):
    """
    Read a Markdown file with encoding detection
    
    Args:
        file_path (str): Path to the Markdown file
        
    Returns:
        str: The content of the Markdown file
        
    Raises:
        FileNotFoundError: If the file does not exist
        IOError: If there is an error reading the file
    """
```

## Parameters

| Name | Type | Description |
|------|------|-------------|
| `file_path` | `str` | Path to the Markdown file to read |

## Return Value

Returns a `str` containing the content of the Markdown file.

## Exceptions

- `FileNotFoundError`: Raised if the specified file does not exist
- `IOError`: Raised if there is an error reading the file
- `UnicodeDecodeError`: Caught internally, function will try alternative encodings

## Detailed Description

This function reads a Markdown file and returns its content as a string. It includes robust error handling and encoding detection to handle files with different character encodings.

The function performs the following operations:

1. Attempts to read the file using UTF-8 encoding (the most common for Markdown files)
2. If UTF-8 decoding fails, tries alternative encodings:
   - big5 (for Chinese characters)
   - latin-1 (as a fallback that can decode any byte sequence)
3. Catches and logs any errors that occur during the reading process
4. Returns the file content as a string if successful

The function is designed to be resilient against common file reading issues, making it suitable for batch processing of files that may have been created with different text editors or on different platforms.

## Example

```python
# Read a Markdown file
try:
    content = read_markdown_file("./README.md")
    print(f"Successfully read file with {len(content)} characters")
except Exception as e:
    print(f"Error reading file: {e}")
```

## Related Functions

- [write_markdown_file](./write-markdown-file.md) - Write content to a Markdown file 