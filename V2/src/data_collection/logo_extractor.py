import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from src.utils.image_utils import download_image, convert_to_png, svg_to_png

def extract_images_from_webpage(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        images = []
        
        # Look for all img tags
        for img in soup.find_all('img'):
            if 'src' in img.attrs:
                img_url = urljoin(url, img['src'])
                image = download_image(img_url)
                if image:
                    images.append(convert_to_png(image))
        
        # Look for SVG images
        for svg in soup.find_all('svg'):
            svg_content = str(svg)
            png_image = svg_to_png(svg_content)
            if png_image:
                images.append(png_image)
        
        return images
    except requests.exceptions.RequestException as e:
        print(f"Error extracting images from {url}: {e}")
        return []

def extract_logo_from_webpage(url):
    images = extract_images_from_webpage(url)
    
    # Look for common logo classes or IDs
    logo_keywords = ['logo', 'brand', 'company', 'site-logo']
    
    for image in images:
        for keyword in logo_keywords:
            if keyword in str(image).lower():
                return image
    
    # If no logo is found, return the first image (if any)
    return images[0] if images else None