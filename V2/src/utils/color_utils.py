import re
import colorsys
import math
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color

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

def rgb_to_lab(rgb_color):
    """Convert RGB color to Lab color space."""
    rgb_color = [x/255 for x in rgb_color]  # Normalize RGB values
    srgb = sRGBColor(*rgb_color)
    lab = convert_color(srgb, LabColor)
    return lab

def delta_e_cie2000(lab1, lab2, kL=1, kC=1, kH=1):
    """
    Calculates the Delta E (CIE2000) of two colors in the Lab color space.
    """
    L1, a1, b1 = lab1.lab_l, lab1.lab_a, lab1.lab_b
    L2, a2, b2 = lab2.lab_l, lab2.lab_a, lab2.lab_b

    C1 = math.sqrt(a1**2 + b1**2)
    C2 = math.sqrt(a2**2 + b2**2)
    C_avg = (C1 + C2) / 2

    G = 0.5 * (1 - math.sqrt(C_avg**7 / (C_avg**7 + 25**7)))

    a1_prime = a1 * (1 + G)
    a2_prime = a2 * (1 + G)

    C1_prime = math.sqrt(a1_prime**2 + b1**2)
    C2_prime = math.sqrt(a2_prime**2 + b2**2)

    h1_prime = math.atan2(b1, a1_prime) % (2 * math.pi)
    h2_prime = math.atan2(b2, a2_prime) % (2 * math.pi)

    delta_L_prime = L2 - L1
    delta_C_prime = C2_prime - C1_prime

    if C1_prime * C2_prime == 0:
        delta_h_prime = 0
    else:
        if abs(h2_prime - h1_prime) <= math.pi:
            delta_h_prime = h2_prime - h1_prime
        elif h2_prime - h1_prime > math.pi:
            delta_h_prime = h2_prime - h1_prime - 2 * math.pi
        else:
            delta_h_prime = h2_prime - h1_prime + 2 * math.pi

    delta_H_prime = 2 * math.sqrt(C1_prime * C2_prime) * math.sin(delta_h_prime / 2)

    L_avg = (L1 + L2) / 2
    C_avg_prime = (C1_prime + C2_prime) / 2

    if C1_prime * C2_prime == 0:
        h_avg_prime = h1_prime + h2_prime
    else:
        if abs(h1_prime - h2_prime) <= math.pi:
            h_avg_prime = (h1_prime + h2_prime) / 2
        elif h1_prime + h2_prime < 2 * math.pi:
            h_avg_prime = (h1_prime + h2_prime + 2 * math.pi) / 2
        else:
            h_avg_prime = (h1_prime + h2_prime - 2 * math.pi) / 2

    T = (1 - 0.17 * math.cos(h_avg_prime - math.pi/6)
         + 0.24 * math.cos(2 * h_avg_prime)
         + 0.32 * math.cos(3 * h_avg_prime + math.pi/30)
         - 0.20 * math.cos(4 * h_avg_prime - 63 * math.pi/180))

    delta_theta = 30 * math.exp(-(((h_avg_prime - 275 * math.pi/180) / (25 * math.pi/180))**2))

    R_C = 2 * math.sqrt(C_avg_prime**7 / (C_avg_prime**7 + 25**7))
    S_L = 1 + (0.015 * (L_avg - 50)**2) / math.sqrt(20 + (L_avg - 50)**2)
    S_C = 1 + 0.045 * C_avg_prime
    S_H = 1 + 0.015 * C_avg_prime * T
    R_T = -math.sin(2 * delta_theta) * R_C

    delta_E = math.sqrt(
        (delta_L_prime / (kL * S_L))**2 +
        (delta_C_prime / (kC * S_C))**2 +
        (delta_H_prime / (kH * S_H))**2 +
        R_T * (delta_C_prime / (kC * S_C)) * (delta_H_prime / (kH * S_H))
    )

    return delta_E

def check_color_similarity(color1, color2):
    """Returns a float between 0 and 1 to represent color similarity"""
    try:
        lab1 = rgb_to_lab(convert_to_rgb(color1))
        lab2 = rgb_to_lab(convert_to_rgb(color2))
        delta_e = delta_e_cie2000(lab1, lab2)
        # Normalize delta_e to a 0-1 scale (assuming max delta_e is 100)
        similarity = 1 - min(delta_e / 100, 1)
        return similarity
    except ValueError as e:
        print(f"Error in check_color_similarity: {e}")
        return 0  # Return 0 similarity for invalid colors