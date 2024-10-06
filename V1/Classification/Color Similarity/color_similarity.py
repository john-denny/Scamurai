import re
import colorsys
import requests
from bs4 import BeautifulSoup
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
import math

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def hsl_to_rgb(h, s, l):
    h /= 360
    s /= 100
    l /= 100
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return tuple(int(x * 255) for x in (r, g, b))

def convert_to_rgb(color):
    if isinstance(color, tuple):
        if len(color) >= 3:
            return color[:3]  # Return the first 3 elements (R, G, B)
        else:
            raise ValueError(f"Invalid tuple length for color: {color}")
    elif isinstance(color, str):
        color = color.strip()
        if color.startswith('#'):
            return hex_to_rgb(color)
        elif color.startswith('rgb'):
            values = re.findall(r'\d+', color)
            if len(values) >= 3:
                return tuple(map(int, values[:3]))
            else:
                raise ValueError(f"Invalid RGB(A) color: {color}")
        elif color.startswith('hsl'):
            values = re.findall(r'\d+', color)
            if len(values) >= 3:
                return hsl_to_rgb(*map(float, values[:3]))
            else:
                raise ValueError(f"Invalid HSL(A) color: {color}")
    raise ValueError(f"Unable to convert color: {color}")

def rgb_to_lab(rgb):
    rgb_color = sRGBColor(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    lab_color = convert_color(rgb_color, LabColor)
    return lab_color

def delta_e_cie2000_custom(lab1, lab2):
    l1, a1, b1 = lab1.lab_l, lab1.lab_a, lab1.lab_b
    l2, a2, b2 = lab2.lab_l, lab2.lab_a, lab2.lab_b
    
    kl, kc, kh = 1, 1, 1
    
    delta_l_prime = l2 - l1
    l_bar = (l1 + l2) / 2
    
    c1 = math.sqrt(a1**2 + b1**2)
    c2 = math.sqrt(a2**2 + b2**2)
    c_bar = (c1 + c2) / 2
    
    a_prime_1 = a1 + (a1 / 2) * (1 - math.sqrt(c_bar**7 / (c_bar**7 + 25**7)))
    a_prime_2 = a2 + (a2 / 2) * (1 - math.sqrt(c_bar**7 / (c_bar**7 + 25**7)))
    
    c_prime_1 = math.sqrt(a_prime_1**2 + b1**2)
    c_prime_2 = math.sqrt(a_prime_2**2 + b2**2)
    c_bar_prime = (c_prime_1 + c_prime_2) / 2
    delta_c_prime = c_prime_2 - c_prime_1
    
    h_prime_1 = math.atan2(b1, a_prime_1) % (2 * math.pi)
    h_prime_2 = math.atan2(b2, a_prime_2) % (2 * math.pi)
    
    delta_h_prime = 0
    if abs(h_prime_1 - h_prime_2) <= math.pi:
        delta_h_prime = h_prime_2 - h_prime_1
    elif h_prime_2 <= h_prime_1:
        delta_h_prime = h_prime_2 - h_prime_1 + 2 * math.pi
    else:
        delta_h_prime = h_prime_2 - h_prime_1 - 2 * math.pi
    
    delta_H_prime = 2 * math.sqrt(c_prime_1 * c_prime_2) * math.sin(delta_h_prime / 2)
    
    T = (1 -
         0.17 * math.cos(h_prime_1 - math.pi/6) +
         0.24 * math.cos(2 * h_prime_1) +
         0.32 * math.cos(3 * h_prime_1 + math.pi/30) -
         0.20 * math.cos(4 * h_prime_1 - 63 * math.pi/180))
    
    sl = 1 + (0.015 * (l_bar - 50)**2) / math.sqrt(20 + (l_bar - 50)**2)
    sc = 1 + 0.045 * c_bar_prime
    sh = 1 + 0.015 * c_bar_prime * T
    
    rt = (-2 * math.sqrt(c_bar_prime**7 / (c_bar_prime**7 + 25**7)) *
          math.sin(60 * math.pi / 180 *
                   math.exp(-((h_prime_1 * 180 / math.pi - 275) / 25)**2)))
    
    return math.sqrt(
        (delta_l_prime / (kl * sl))**2 +
        (delta_c_prime / (kc * sc))**2 +
        (delta_H_prime / (kh * sh))**2 +
        rt * (delta_c_prime / (kc * sc)) * (delta_H_prime / (kh * sh))
    )

def check_color_similarity(color1, color2):
    """Returns a float between 0 and 1 to represent color similarity"""
    try:
        lab1 = rgb_to_lab(convert_to_rgb(color1))
        lab2 = rgb_to_lab(convert_to_rgb(color2))
        delta_e = delta_e_cie2000_custom(lab1, lab2)
        # Normalize delta_e to a 0-1 scale (assuming max delta_e is 100)
        similarity = 1 - min(delta_e / 100, 1)
        return similarity
    except ValueError as e:
        print(f"Error in check_color_similarity: {e}")
        return 0  # Return 0 similarity for invalid colors

def extract_colors_from_css(url, css_url):
    response = requests.get(css_url)
    response.raise_for_status()
    css_content = response.text

    # Regex to find color values in CSS
    color_regex = re.compile(r'#[0-9a-fA-F]{3,6}|rgba?\([^)]+\)|hsla?\([^)]+\)')
    return color_regex.findall(css_content)

def extract_colors_from_webpage(url):
    # Fetch the webpage content
    response = requests.get(url)
    response.raise_for_status()
    
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
        if style.string:
            colors.extend(color_regex.findall(style.string))
    
    # Extract colors from inline styles
    for tag in inline_styles:
        colors.extend(color_regex.findall(tag['style']))
    
    # Find all external CSS links
    css_links = [link['href'] for link in soup.find_all('link', rel='stylesheet') if 'href' in link.attrs]
    
    # Fetch and extract colors from each CSS file
    for css_link in css_links:
        if css_link.startswith('http'):
            css_url = css_link
        else:
            css_url = requests.compat.urljoin(url, css_link)
        colors.extend(extract_colors_from_css(url, css_url))
    
    return colors

def find_similar_colors(extracted_colors, colors_to_test, threshold=0.9):
    similar_colors = []
    for test_color in colors_to_test:
        for extracted_color in extracted_colors:
            similarity = check_color_similarity(test_color, extracted_color)
            if similarity >= threshold:
                similar_colors.append((test_color, extracted_color, similarity))
    return similar_colors

# Example usagez
url = 'https://www.google.com/'  # Replace with your target URL
colors_to_test = ['#FF0000', 'rgb(0, 255, 0)', 'hsl(240, 100%, 50%)'] # Insert Profile of colors here

extracted_colors = extract_colors_from_webpage(url)
print("Extracted colors:", extracted_colors)

if not extracted_colors:
    print("No colors were extracted from the webpage.")
else:
    similar_colors = find_similar_colors(extracted_colors, colors_to_test)
    print("\nSimilar colors found:")
    for test_color, extracted_color, similarity in similar_colors:
        print(f"Test color: {test_color}, Extracted color: {extracted_color}, Similarity: {similarity:.2f}")
