import requests
from bs4 import BeautifulSoup
import re
from src.utils.color_utils import convert_to_rgb, rgb_to_lab
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from collections import Counter

def extract_colors_from_webpage(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        color_regex = re.compile(r'#[0-9a-fA-F]{3,6}|rgba?\([^)]+\)|hsla?\([^)]+\)')
        
        colors = []
        
        # Extract colors from style tags
        for style in soup.find_all('style'):
            if style.string:
                colors.extend(color_regex.findall(style.string))
        
        # Extract colors from inline styles
        for tag in soup.find_all(style=True):
            colors.extend(color_regex.findall(tag['style']))
        
        # Extract colors from external CSS files
        for link in soup.find_all('link', rel='stylesheet'):
            if 'href' in link.attrs:
                css_url = requests.compat.urljoin(url, link['href'])
                colors.extend(extract_colors_from_css(css_url))
        
        return colors
    except requests.exceptions.RequestException as e:
        print(f"Error fetching webpage: {e}")
        return []

def extract_colors_from_css(css_url):
    try:
        response = requests.get(css_url, timeout=10)
        response.raise_for_status()
        color_regex = re.compile(r'#[0-9a-fA-F]{3,6}|rgba?\([^)]+\)|hsla?\([^)]+\)')
        return color_regex.findall(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching CSS file: {e}")
        return []

def get_dominant_colors(colors, num_colors=5):
    # Convert all colors to RGB format
    rgb_colors = [convert_to_rgb(color) for color in colors]
    
    # Convert RGB colors to Lab color space
    lab_colors = [rgb_to_lab(rgb) for rgb in rgb_colors]
    
    # Count occurrences of each color
    color_counts = {}
    for lab in lab_colors:
        key = (round(lab.lab_l, 2), round(lab.lab_a, 2), round(lab.lab_b, 2))
        color_counts[key] = color_counts.get(key, 0) + 1
    
    # Sort colors by count in descending order
    sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Get the top num_colors
    dominant_colors = [item[0] for item in sorted_colors[:num_colors]]
    
    # Convert Lab colors back to RGB for easier use
    dominant_rgb = [convert_color(LabColor(*lab), sRGBColor).get_value_tuple() for lab in dominant_colors]
    
    return [(int(r * 255), int(g * 255), int(b * 255)) for r, g, b in dominant_rgb]

if __name__ == "__main__":
    # Example usage
    url = "https://example.com"
    extracted_colors = extract_colors_from_webpage(url)
    dominant_colors = get_dominant_colors(extracted_colors)
    print("Dominant colors:", dominant_colors)