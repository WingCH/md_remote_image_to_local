# File Utilities Module Overview

The File Utilities Module provides functionality for file operations, including reading and writing Markdown files, handling file paths, and managing directory structures. These functions support the core image processing operations by ensuring proper file handling.

## Main Features

- Reading Markdown files with encoding detection
- Writing updated Markdown content back to files
- Creating and managing directory structures for image storage
- Calculating relative paths for image references

## Available Functions

A complete list of functions can be found in the [File Utilities Functions List](./list.md).

### Key Functions:

- [read_markdown_file](./read-markdown-file.md) - Read a Markdown file with encoding detection
- [write_markdown_file](./write-markdown-file.md) - Write content to a Markdown file
- [create_resources_directory](./create-resources-directory.md) - Create a resources directory for image storage
- [calculate_relative_path](./calculate-relative-path.md) - Calculate relative path between two file locations

## Usage Example

```python
# Read a Markdown file
content = read_markdown_file("./example.md")

# Process content...

# Create resources directory
resources_dir = create_resources_directory("./example.md")

# Write updated content back to the file
write_markdown_file("./example.md", updated_content)
``` 