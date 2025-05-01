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
import concurrent.futures
from tqdm import tqdm


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


def download_image(url_info):
    """Download image and return the save path
    
    Args:
        url_info: tuple containing (url, save_dir)
    
    Returns:
        tuple: (url, filepath or None)
    """
    url, save_dir = url_info
    
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
        return (url, filepath)
    except Exception as e:
        tqdm.write(f"Failed to download image: {url}, error: {e}")
        return (url, None)


def batch_download_images(urls, save_dir, max_workers=10):
    """Download multiple images in parallel
    
    Args:
        urls: List of image URLs
        save_dir: Directory to save images
        max_workers: Maximum number of parallel downloads
    
    Returns:
        dict: Mapping of URLs to local file paths
    """
    url_to_path = {}
    
    # Create a list of tuples (url, save_dir) for each URL
    download_tasks = [(url, save_dir) for url in urls]
    
    # Use ThreadPoolExecutor for parallel downloads with progress bar
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Use as_completed to process concurrent tasks
        futures = {executor.submit(download_image, task): task for task in download_tasks}
        
        # Use tqdm to display task completion progress
        for future in tqdm(
            concurrent.futures.as_completed(futures),
            total=len(futures),
            desc="Downloading images",
            unit="img",
            leave=True  # Ensure progress bar remains after completion
        ):
            url, save_dir = futures[future]
            try:
                url, filepath = future.result()
                if filepath:
                    url_to_path[url] = filepath
            except Exception as e:
                tqdm.write(f"Error downloading {url}: {e}")
    
    return url_to_path


def process_markdown_file(file_path, target_dir, max_workers=10):
    """Process a single Markdown file, download remote images and update paths
    
    Returns:
        tuple: (images_found, images_updated) - Number of found images and successfully updated images
    """
    # Use tqdm.write instead of print to avoid interfering with progress bar display
    tqdm.write(f"Processing file: {file_path}")
    
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
            tqdm.write(f"Unable to read file {file_path}: {e}")
            return 0, 0
    except Exception as e:
        tqdm.write(f"Error while reading file {file_path}: {e}")
        return 0, 0
    
    # Extract image URLs
    image_urls = extract_image_urls(content)
    
    if not image_urls:
        tqdm.write(f"No remote images found in {file_path}")
        return 0, 0
    
    images_found = len(image_urls)
    tqdm.write(f"Found {images_found} remote images in {file_path}")
    
    # Create resource directory for the current Markdown file
    md_file_dir = os.path.dirname(os.path.abspath(file_path))
    resources_dir = os.path.join(md_file_dir, "resources")
    
    # Batch download images
    url_to_path_map = batch_download_images(image_urls, resources_dir, max_workers)
    
    # Update Markdown content
    modified_content = content
    images_updated = 0
    
    for url, local_path in url_to_path_map.items():
        if local_path:
            # Calculate relative path
            rel_path = os.path.relpath(local_path, md_file_dir)
            rel_path = rel_path.replace('\\', '/')  # Ensure path separators are consistent
            
            # Update image URLs in Markdown
            # Handle standard Markdown image format
            pattern = f'!\\[(.*?)\\]\\({re.escape(url)}\\)'
            new_content = re.sub(pattern, lambda m: f'![{m.group(1)}]({rel_path})', modified_content)
            
            # Handle HTML tag format
            pattern = f'<img([^>]*)src=[\'"]({re.escape(url)})[\'"]([^>]*)>'
            new_content = re.sub(pattern, lambda m: f'<img{m.group(1)}src="{rel_path}"{m.group(3)}>', new_content)
            
            # Check if any replacements were made
            if new_content != modified_content:
                modified_content = new_content
                images_updated += 1
    
    # Save modified Markdown file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        tqdm.write(f"Completed processing {file_path}, updated {images_updated} image references (out of {images_found} found)")
    except Exception as e:
        tqdm.write(f"Error while writing file {file_path}: {e}")
    
    return images_found, images_updated


def process_directory(target_dir, max_workers=10):
    """Process all Markdown files in the target directory"""
    # Get all Markdown files
    markdown_files = glob.glob(os.path.join(target_dir, "**/*.md"), recursive=True)
    
    if not markdown_files:
        tqdm.write(f"No Markdown files found in {target_dir}")
        return
    
    tqdm.write(f"Found {len(markdown_files)} Markdown files in {target_dir}")
    
    # Track total number of images and successfully downloaded images
    total_images_found = 0
    total_images_updated = 0
    
    # Process files with progress bar
    for file_path in tqdm(markdown_files, desc="Processing files", unit="file", leave=True):
        images_found, images_updated = process_markdown_file(file_path, target_dir, max_workers)
        total_images_found += images_found
        total_images_updated += images_updated
    
    # Summary report
    tqdm.write(f"\nSummary:")
    tqdm.write(f"Total remote images found: {total_images_found}")
    tqdm.write(f"Total images successfully downloaded and updated: {total_images_updated}")
    if total_images_found > total_images_updated:
        tqdm.write(f"Images failed to download or update: {total_images_found - total_images_updated}")
    
    tqdm.write("Completed processing all Markdown files")


def main():
    
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Download remote images in Markdown files and replace with local paths')
    parser.add_argument('target_dir', help='Target directory (containing Markdown files)')
    parser.add_argument('-w', '--workers', type=int, default=10, help='Maximum number of parallel downloads (default: 10)')
    
    args = parser.parse_args()
    target_dir = os.path.abspath(args.target_dir)
    max_workers = args.workers
    
    # Check if target directory exists
    if not os.path.isdir(target_dir):
        print(f"Error: Target directory '{target_dir}' does not exist")
        sys.exit(1)
    
    # Process target directory
    process_directory(target_dir, max_workers)


if __name__ == "__main__":
    main() 