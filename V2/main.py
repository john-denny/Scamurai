import tempfile
import os
from PIL import Image

from src.config.company_profiles import COMPANY_PROFILES
from src.data_collection.color_extractor import extract_colors_from_webpage, get_dominant_colors
from src.data_collection.domain_analyzer import analyze_domain
from src.data_collection.logo_extractor import extract_logo_from_webpage
from src.comparison.color_comparison import compare_colors
from src.comparison.domain_comparison import compare_domains
from src.comparison.logo_comparison import compare_logos

# TODO Need to remove most common colors/improve the profiles
# TODO Need to fix the logo comparison system with its installs


def analyze_website(url, company_profile):
    # Extract and analyze colors
    extracted_colors = extract_colors_from_webpage(url)
    dominant_colors = get_dominant_colors(extracted_colors)
    color_similarities = compare_colors(dominant_colors, company_profile['colors'])
    
    # Analyze domain
    domain = url.split('//')[-1].split('/')[0]
    analyzed_domain = analyze_domain(domain)
    domain_similarities = compare_domains(analyzed_domain, company_profile['domains'])
    
    # Extract and compare logo
    extracted_logo = extract_logo_from_webpage(url)
    logo_similarity = None
    if extracted_logo:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_logo_path = os.path.join(temp_dir, "extracted_logo.png")
            extracted_logo.save(temp_logo_path)
            logo_similarity = compare_logos(temp_dir, company_profile['logo_directory'])
    
    return {
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

if __name__ == "__main__":
    main()