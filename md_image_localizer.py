#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import glob
import argparse
import urllib.request
import urllib.parse
import uuid
import shutil
from pathlib import Path


def is_url(string):
    """Check if a string is a URL"""
    return string.startswith(('http://', 'https://', 'ftp://'))


def is_image_url(url):
    """Check if a URL is an image"""
    image_extensions = ['.image', '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg']
    parsed_url = urllib.parse.urlparse(url)
    path = parsed_url.path.lower()
    
    # Check if the path ends with an image extension
    path_has_extension = any(path.endswith(ext) for ext in image_extensions)
    
    # Check if URL contains specific image service characteristics
    known_image_hosts = ['i.imgur.com', 'p3-juejin.byteimg.com', 'cdn.pixabay.com', 'images.unsplash.com']
    is_known_host = parsed_url.netloc in known_image_hosts
    
    # Check if URL contains image-related parameters
    has_image_param = 'image' in url.lower() or 'img' in url.lower() or 'pic' in url.lower()
    
    return path_has_extension or is_known_host or has_image_param


def extract_image_urls(markdown_content):
    """Extract image URLs from Markdown content"""
    # Standard Markdown image format: ![alt](url) or ![](url)
    standard_pattern = r'!\[(.*?)\]\((https?://[^)]+)\)'
    
    # HTML tag format: <img src="url" />
    html_pattern = r'<img[^>]*src=[\'"]([^\'"]+)[\'"][^>]*>'
    
    # Combine results from both patterns
    urls = []
    
    for pattern in [standard_pattern, html_pattern]:
        matches = re.findall(pattern, markdown_content)
        for match in matches:
            # Standard Markdown pattern returns tuples with (alt_text, url)
            if isinstance(match, tuple) and len(match) > 1:
                url = match[1]  # Use the second element (URL)
            else:
                url = match
            
            # Skip non-URL matches
            if not is_url(url):
                continue
                
            # Only include image URLs
            if is_image_url(url):
                urls.append(url)
    
    return urls


def download_image(url, save_dir):
    """Download image and return the save path"""
    # Create save directory (if it doesn't exist)
    os.makedirs(save_dir, exist_ok=True)
    
    # Get filename from URL
    parsed_url = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    # If filename is empty or invalid, generate a random filename
    if not filename or len(filename) < 3:
        extension = ".jpg"  # Default extension
        filename = f"{uuid.uuid4()}{extension}"
    
    # Ensure filename is unique
    filepath = os.path.join(save_dir, filename)
    counter = 1
    while os.path.exists(filepath):
        name, ext = os.path.splitext(filename)
        filepath = os.path.join(save_dir, f"{name}_{counter}{ext}")
        counter += 1
    
    try:
        # Download image
        urllib.request.urlretrieve(url, filepath)
        print(f"Downloaded image: {url} -> {filepath}")
        return filepath
    except Exception as e:
        print(f"Failed to download image: {url}, error: {e}")
        return None


def process_markdown_file(file_path, target_dir):
    """Process a single Markdown file, download remote images and update paths
    
    Returns:
        tuple: (images_found, images_updated) - Number of found images and successfully updated images
    """
    print(f"Processing file: {file_path}")
    
    # Read Markdown file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Try different encoding
        try:
            with open(file_path, 'r', encoding='big5') as f:
                content = f.read()
        except Exception as e:
            print(f"Unable to read file {file_path}: {e}")
            return 0, 0
    except Exception as e:
        print(f"Error while reading file {file_path}: {e}")
        return 0, 0
    
    # Extract image URLs
    image_urls = extract_image_urls(content)
    
    if not image_urls:
        print(f"No remote images found in {file_path}")
        return 0, 0
    
    images_found = len(image_urls)
    print(f"Found {images_found} remote images in {file_path}")
    
    # Create resource directory for the current Markdown file
    md_file_dir = os.path.dirname(os.path.abspath(file_path))
    resources_dir = os.path.join(md_file_dir, "resources")
    
    # Download images and update Markdown content
    modified_content = content
    images_updated = 0  # Count successfully downloaded and replaced images
    
    for url in image_urls:
        local_path = download_image(url, resources_dir)
        
        if local_path:
            # Calculate relative path
            rel_path = os.path.relpath(local_path, md_file_dir)
            rel_path = rel_path.replace('\\', '/')  # Ensure path separators are consistent
            
            # Update image URLs in Markdown
            # Handle standard Markdown image format
            pattern = f'!\\[(.*?)\\]\\({re.escape(url)}\\)'
            new_content = re.sub(pattern, f'![\g<1>]({rel_path})', modified_content)
            
            # Handle HTML tag format
            pattern = f'<img([^>]*)src=[\'"]({re.escape(url)})[\'"]([^>]*)>'
            new_content = re.sub(pattern, f'<img\g<1>src="{rel_path}"\g<3>>', new_content)
            
            # Check if any replacements were made
            if new_content != modified_content:
                modified_content = new_content
                images_updated += 1
    
    # Save modified Markdown file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        print(f"Completed processing {file_path}, updated {images_updated} image references (out of {images_found} found)")
    except Exception as e:
        print(f"Error while writing file {file_path}: {e}")
    
    return images_found, images_updated


def process_directory(target_dir):
    """Process all Markdown files in the target directory"""
    # Get all Markdown files
    markdown_files = glob.glob(os.path.join(target_dir, "**/*.md"), recursive=True)
    
    if not markdown_files:
        print(f"No Markdown files found in {target_dir}")
        return
    
    print(f"Found {len(markdown_files)} Markdown files in {target_dir}")
    
    # Track total number of images and successfully downloaded images
    total_images_found = 0
    total_images_updated = 0
    
    for file_path in markdown_files:
        images_found, images_updated = process_markdown_file(file_path, target_dir)
        total_images_found += images_found
        total_images_updated += images_updated
    
    # Summary report
    print(f"\nSummary:")
    print(f"Total remote images found: {total_images_found}")
    print(f"Total images successfully downloaded and updated: {total_images_updated}")
    if total_images_found > total_images_updated:
        print(f"Images failed to download or update: {total_images_found - total_images_updated}")
    
    print("Completed processing all Markdown files")


def main():
    
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Download remote images in Markdown files and replace with local paths')
    parser.add_argument('target_dir', help='Target directory (containing Markdown files)')
    
    args = parser.parse_args()
    target_dir = os.path.abspath(args.target_dir)
    
    # Check if target directory exists
    if not os.path.isdir(target_dir):
        print(f"Error: Target directory '{target_dir}' does not exist")
        sys.exit(1)
    
    # Process target directory
    process_directory(target_dir)


if __name__ == "__main__":
    main() 