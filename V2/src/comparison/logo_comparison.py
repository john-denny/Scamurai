import os
from src.utils.image_utils import compare_images

def compare_logos(extracted_logos_dir, profile_logo_directory, threshold=0.7):
    if not os.path.isdir(extracted_logos_dir) or not os.path.isdir(profile_logo_directory):
        return None
    
    matching_logos = []
    
    for extracted_logo in os.listdir(extracted_logos_dir):
        extracted_logo_path = os.path.join(extracted_logos_dir, extracted_logo)
        max_similarity = 0
        
        for profile_logo in os.listdir(profile_logo_directory):
            profile_logo_path = os.path.join(profile_logo_directory, profile_logo)
            if os.path.isfile(profile_logo_path):
                similarity = compare_images(extracted_logo_path, profile_logo_path)
                max_similarity = max(max_similarity, similarity)
        
        if max_similarity >= threshold:
            matching_logos.append(extracted_logo_path)
        else:
            os.remove(extracted_logo_path)
    
    return matching_logos if matching_logos else None