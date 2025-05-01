# Markdown Remote Image to Local Tool Requirements

## Functional Requirements

1. **Virtual Environment Check**
   - Check if the script is running in a virtual environment
   - If not in a virtual environment, automatically create one and install required dependencies

2. **Markdown File Processing**
   - Read all Markdown files in the target directory
   - Identify remote image links in the files

3. **Image Processing**
   - Download identified remote images
   - Create a "resources" folder in the target directory
   - Save downloaded images to the resources folder

4. **Markdown Update**
   - Update image paths in Markdown files
   - Replace remote URLs with local relative paths

## Technical Requirements

1. Developed using Python
2. Support for automatic creation and management of virtual environments
3. Support for parsing and modifying Markdown format
4. Support for downloading and local storage of network images 