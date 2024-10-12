import requests
from PIL import Image, UnidentifiedImageError
import io
import cairosvg
import cv2
import numpy as np

def download_image(url):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        
        content_type = response.headers.get('Content-Type', '')
        
        img = Image.open(io.BytesIO(response.content))
        return img
    except requests.RequestException as e:
        print(f"Error downloading image from {url}: {e}")
    except UnidentifiedImageError:
        # Check if it's an SVG
        if content_type == 'image/svg+xml' or url.lower().endswith('.svg'):
            try:
                svg_content = response.content
                return svg_to_png(svg_content)
            except Exception as svg_error:
                print(f"Error converting SVG to PNG: {svg_error}")
        else:
            print(f"Cannot identify image from {url}")
    except Exception as e:
        print(f"Unexpected error processing image from {url}: {e}")
    
    return None

def convert_to_png(image):
    if image.format != 'PNG':
        return image.convert('RGBA')
    return image

def svg_to_png(svg_content, width=None, height=None):
    try:
        # Convert SVG to PNG without specifying width and height
        png_data = cairosvg.svg2png(bytestring=svg_content)
        img = Image.open(io.BytesIO(png_data))
        
        # Resize the image if width or height is specified
        if width or height:
            img.thumbnail((width or img.width, height or img.height))
        
        return img
    except Exception as e:
        print(f"Error converting SVG to PNG: {e}")
        return None

def compare_images(img1_path, img2_path):
    # Load images
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    
    # Check if images are loaded successfully
    if img1 is None or img2 is None:
        print(f"Error loading images: {img1_path} or {img2_path}")
        return 0  # Return 0 similarity if images can't be loaded
    
    # Resize images to have the same dimensions
    height = min(img1.shape[0], img2.shape[0])
    width = min(img1.shape[1], img2.shape[1])
    img1 = cv2.resize(img1, (width, height))
    img2 = cv2.resize(img2, (width, height))
    
    # Convert images to HSV color space
    img1_hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    img2_hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    
    # Calculate histograms
    hist1 = cv2.calcHist([img1_hsv], [0, 1, 2], None, [8, 8, 8], [0, 180, 0, 256, 0, 256])
    hist2 = cv2.calcHist([img2_hsv], [0, 1, 2], None, [8, 8, 8], [0, 180, 0, 256, 0, 256])
    
    # Normalize histograms
    cv2.normalize(hist1, hist1, 0, 1, cv2.NORM_MINMAX)
    cv2.normalize(hist2, hist2, 0, 1, cv2.NORM_MINMAX)
    
    # Compare histograms
    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    
    return similarity

def extract_dominant_color(image, num_colors=1):
    if image is None:
        return None
    image = image.convert('RGB')
    image = image.resize((100, 100))
    pixels = list(image.getdata())
    
    color_counts = {}
    for pixel in pixels:
        if pixel in color_counts:
            color_counts[pixel] += 1
        else:
            color_counts[pixel] = 1
    
    sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
    return [color for color, _ in sorted_colors[:num_colors]]

def save_image(image, filepath):
    if image is None:
        print(f"Cannot save image to {filepath}: Image is None")
        return
    try:
        image.save(filepath)
        print(f"Image saved successfully to {filepath}")
    except Exception as e:
        print(f"Error saving image to {filepath}: {e}")

if __name__ == "__main__":
    # Example usage
    url = "https://www.example.com/image.png"
    downloaded_image = download_image(url)
    
    if downloaded_image:
        save_image(downloaded_image, "downloaded_image.png")
        
        dominant_color = extract_dominant_color(downloaded_image)
        print(f"Dominant color: {dominant_color}")
        
        another_image = Image.open("another_image.png")
        similarity = compare_images(downloaded_image, another_image)
        print(f"Image similarity: {similarity}")
