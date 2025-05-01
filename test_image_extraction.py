#!/usr/bin/env python3
import re
import urllib.parse

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

def test_extraction():
    markdown_content = '![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/13ff4d1ee598430aa26f4b4d1aec3a5e~tplv-k3u1fbpfcp-zoom-1.image)'
    print(f"Testing with content: {markdown_content}")
    
    # Test various regex patterns
    patterns = [
        r'!\[(.*?)\]\((https?://[^)]+)\)',  # Original pattern
        r'!\[(.*?)\]\((https?://[^\s)]+)\)',  # Modified pattern with no spaces
        r'!\[(.*?)\]\((https?://[^"\')]+)\)',  # Pattern for URLs without quotes or parens
        r'!\[(.*?)\]\((https?://[^"\'\s)]+(?:[^\s)]+)*)\)'  # More complex pattern
    ]
    
    for i, pattern in enumerate(patterns):
        print(f"\nPattern {i+1}: {pattern}")
        matches = re.findall(pattern, markdown_content)
        print(f"Matches: {matches}")
        
        if matches:
            for match in matches:
                if isinstance(match, tuple):
                    url = match[1] if len(match) > 1 else match[0]
                    print(f"URL from tuple: {url}")
                else:
                    url = match
                    print(f"URL from string: {url}")
                
                print(f"Is URL: {is_url(url)}")
                print(f"Is image URL: {is_image_url(url)}")

if __name__ == "__main__":
    test_extraction() 