import cv2
import numpy as np
from PIL import Image
import cairosvg
import io

def histogram_similarity(target_image: str, preproccessed_image):
    # TODO BUILD IN IMAGE CONVERSION E.G SVG -> JPG
    if target_image.endswith(".svg"):
        cairosvg.svg2png(url=target_image, write_to="bingchilling-laoganma.png")
        # Read the PNG image from the data
        image = Image.open("bingchilling-laoganma.png")

        if image.mode == 'RGBA':
            
            image = image.convert('RGB')
            image = np.array(image)
            print("Converted from RGBA to RGB")
    else:
        image = cv2.imread(target_image)
        image = np.array(image)
    
    # Load and split the images into R, G, B channels
    b1, g1, r1 = cv2.split(image)
    preproccessed_image = np.array(cv2.imread(preproccessed_image))
    b2, g2, r2 = cv2.split(preproccessed_image)
    
    # Calculate histograms for each channel
    hist_b1 = cv2.calcHist([b1], [0], None, [256], [0, 256])
    hist_g1 = cv2.calcHist([g1], [0], None, [256], [0, 256])
    hist_r1 = cv2.calcHist([r1], [0], None, [256], [0, 256])
    
    hist_b2 = cv2.calcHist([b2], [0], None, [256], [0, 256])
    hist_g2 = cv2.calcHist([g2], [0], None, [256], [0, 256])
    hist_r2 = cv2.calcHist([r2], [0], None, [256], [0, 256])
    
    # Normalize histograms
    hist_b1 /= np.sum(hist_b1)
    hist_g1 /= np.sum(hist_g1)
    hist_r1 /= np.sum(hist_r1)
    hist_b2 /= np.sum(hist_b2)
    hist_g2 /= np.sum(hist_g2)
    hist_r2 /= np.sum(hist_r2)
    
    # Compute correlation coefficient for each channel
    corr_b = np.corrcoef(hist_b1.flatten(), hist_b2.flatten())[0, 1]
    corr_g = np.corrcoef(hist_g1.flatten(), hist_g2.flatten())[0, 1]
    corr_r = np.corrcoef(hist_r1.flatten(), hist_r2.flatten())[0, 1]
    
    # Average the correlation coefficients
    similarity = (corr_b + corr_g + corr_r) / 3
    
    return similarity

# Example usage

similarity = histogram_similarity("logo1.svg", "an-post-logo.jpg")
print(f"Similarity: {similarity:.2f}")
