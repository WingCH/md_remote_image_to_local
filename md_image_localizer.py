#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import glob
import argparse
import venv
import subprocess
import urllib.request
import urllib.parse
import uuid
import shutil
import platform
from pathlib import Path


def check_venv():
    """Check if running in a virtual environment, if not create one and prompt user to activate it"""
    # Check if running in a virtual environment
    in_venv = sys.prefix != sys.base_prefix
    
    if not in_venv:
        print("Not running in a virtual environment!")
        
        # Create virtual environment directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        venv_dir = os.path.join(script_dir, "venv")
        
        # Determine operating system
        is_windows = platform.system() == "Windows"
        
        # If the virtual environment directory doesn't exist, create it
        if not os.path.exists(venv_dir):
            print("Creating virtual environment...")
            try:
                venv.create(venv_dir, with_pip=True)
            except Exception as e:
                print(f"Failed to create virtual environment: {e}")
                print("Please manually run the following commands to create a virtual environment:")
                print(f"python -m venv {venv_dir}")
                sys.exit(1)
            
            # Install required dependencies
            print("Installing required dependencies...")
            pip_path = os.path.join(venv_dir, "bin", "pip") if not is_windows else os.path.join(venv_dir, "Scripts", "pip.exe")
            
            # Confirm pip path exists
            if not os.path.exists(pip_path):
                print(f"Warning: Could not find pip at expected location: {pip_path}")
                if not is_windows:  # macOS/Linux
                    pip_path = os.path.join(venv_dir, "bin", "pip3")
                    if not os.path.exists(pip_path):
                        print("Could not find pip or pip3. Please install dependencies manually:")
                        print(f"source {os.path.join(venv_dir, 'bin', 'activate')}")
                        print(f"pip install -r {os.path.join(script_dir, 'requirements.txt')}")
                        sys.exit(1)
            
            # Install dependencies from requirements.txt
            req_path = os.path.join(script_dir, "requirements.txt")
            if os.path.exists(req_path):
                try:
                    subprocess.check_call([pip_path, "install", "-r", req_path])
                except subprocess.CalledProcessError as e:
                    print(f"Failed to install dependencies: {e}")
                    print("Please install dependencies manually:")
                    print(f"{'source ' if not is_windows else ''}{os.path.join(venv_dir, 'bin' if not is_windows else 'Scripts', 'activate')}")
                    print(f"pip install -r {req_path}")
                    sys.exit(1)
            else:
                print(f"Warning: requirements.txt file not found at {req_path}")
                print("Installing basic dependencies...")
                try:
                    subprocess.check_call([pip_path, "install", "markdown", "requests"])
                except subprocess.CalledProcessError as e:
                    print(f"Failed to install basic dependencies: {e}")
                    sys.exit(1)
        
        # Prompt user how to activate the virtual environment
        if is_windows:
            activate_path = os.path.join(venv_dir, "Scripts", "activate.bat")
            python_path = os.path.join(venv_dir, "Scripts", "python.exe")
        else:  # macOS/Linux
            activate_path = os.path.join(venv_dir, "bin", "activate")
            python_path = os.path.join(venv_dir, "bin", "python")
        
        print("\nPlease activate the virtual environment before running this script:")
        if not is_windows:  # macOS/Linux
            print(f"source {activate_path}")
            print(f"python {os.path.abspath(__file__)} <target_directory>")
        else:  # Windows
            print(f"{activate_path}")
            print(f"{python_path} {os.path.abspath(__file__)} <target_directory>")
        
        sys.exit(0)
    
    print("Running in virtual environment")
    return True


def is_url(string):
    """Check if a string is a URL"""
    return string.startswith(('http://', 'https://', 'ftp://'))


def is_image_url(url):
    """Check if a URL is an image"""
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg']
    parsed_url = urllib.parse.urlparse(url)
    path = parsed_url.path.lower()
    return any(path.endswith(ext) for ext in image_extensions)


def extract_image_urls(markdown_content):
    """Extract image URLs from Markdown content"""
    # Standard Markdown image format: ![alt](url)
    standard_pattern = r'!\[.*?\]\((https?://[^)]+)\)'
    
    # HTML tag format: <img src="url" />
    html_pattern = r'<img[^>]*src=[\'"]([^\'"]+)[\'"][^>]*>'
    
    # Combine results from both patterns
    urls = []
    
    for pattern in [standard_pattern, html_pattern]:
        matches = re.findall(pattern, markdown_content)
        for match in matches:
            if is_url(match) and is_image_url(match):
                urls.append(match)
    
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
    # Check virtual environment
    if not check_venv():
        return
    
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