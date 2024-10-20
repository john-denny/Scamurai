from src.utils.color_utils import check_color_similarity

def compare_colors(extracted_colors, profile_colors, threshold=0.8):
    similarities = []
    for extracted_color in extracted_colors:
        for profile_color in profile_colors:
            similarity = check_color_similarity(extracted_color, profile_color)
            if similarity >= threshold:
                similarities.append((extracted_color, profile_color, similarity))
    return similarities