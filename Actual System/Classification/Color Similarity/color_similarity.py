
import requests
from bs4 import BeautifulSoup
import re

def check_color_similarity(html_text, colors_to_test):
    """Returns a float between 0 and 1 to represent color similarity"""



def extract_colors_from_webpage(url):
    # Fetch the webpage content
    response = requests.get(url)
    response.raise_for_status()
    print(response.text)
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all style tags and inline styles
    styles = soup.find_all('style')
    inline_styles = soup.find_all(style=True)
    
    # Regex to find color values (hex, rgb, rgba, hsl, hsla)
    color_regex = re.compile(r'#[0-9a-fA-F]{3,6}|rgba?\([^)]+\)|hsla?\([^)]+\)')
    
    # Extract colors from style tags
    colors = []
    for style in styles:
        colors.append(color_regex.findall(style.string))
    
    # Extract colors from inline styles
    for tag in inline_styles:
        colors.append(color_regex.findall(tag['style']))
    
    return colors[0]

# Example usage
url = 'https://www.example.com/'  # Replace with your target URL
colors = extract_colors_from_webpage(url)



