import os
import shutil
from PIL import Image

from src.config.company_profiles import COMPANY_PROFILES
from src.data_collection.color_extractor import extract_colors_from_webpage, get_dominant_colors
from src.data_collection.domain_analyzer import analyze_domain
from src.data_collection.logo_extractor import extract_images_from_webpage
from src.comparison.color_comparison import compare_colors
from src.comparison.domain_comparison import compare_domains
from src.comparison.logo_comparison import compare_logos
from src.data_collection.domain_ager import is_domain_young
from src.utils.report_writer import save_report
from src.utils.image_utils import save_image

TEMP_DIR = './temp'

def analyze_website(url, company_profile):
    # Extract and analyze colors
    extracted_colors = extract_colors_from_webpage(url)
    dominant_colors = get_dominant_colors(extracted_colors)
    color_similarities = compare_colors(dominant_colors, company_profile['colors'])
    domain_less_than_90_days = is_domain_young(url)
    
    # Analyze domain
    domain = url.split('//')[-1].split('/')[0]
    analyzed_domain = analyze_domain(domain)
    domain_similarities = compare_domains(analyzed_domain, company_profile['domains'])
    
    # Extract and compare logo
    extracted_logos = extract_images_from_webpage(url)
    logo_similarity = None
    if extracted_logos:
        
        os.makedirs(TEMP_DIR, exist_ok=True)
        for i, image in enumerate(extracted_logos):
            temp_logo_path = os.path.join(TEMP_DIR, f"extracted_logo_{i}.png")
            save_image(image, temp_logo_path)
        logo_similarity = compare_logos(TEMP_DIR, company_profile['logo_directory'])
    
    
    
    return {
        'domain_less_than_90_days': domain_less_than_90_days,
        'color_similarities': color_similarities,
        'domain_similarities': domain_similarities,
        'logo_similarity': logo_similarity
    }

def main():
    url_to_analyze = input("Enter the URL to analyze: ")
    company_name = input("Enter the company name to compare against: ")

    if company_name not in COMPANY_PROFILES:
        print(f"Error: Company profile for {company_name} not found.")
        return

    company_profile = COMPANY_PROFILES[company_name]
    results = analyze_website(url_to_analyze, company_profile)

    print("Analysis Results:")
    print("Color Similarities:", results['color_similarities'])
    print("Domain Similarities:", results['domain_similarities'])
    print("Logo Similarity:", results['logo_similarity'])

    # Ask the user if they want to save the report
    user_request = input("Do you want to save the report? (y/n): ")
    if "y" in user_request.lower():
        save_report(results, url_to_analyze, company_name)
    else:
        print("Report not saved.")
    # Clear the temp directory
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)

if __name__ == "__main__":
    main()
