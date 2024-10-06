
# A functional wrapper for All functions built in the project. Takes in a domain and returns whether it is a phishing site or not.
import dns.resolver
import whois
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import cv2
import numpy as np
from PIL import Image
import cairosvg
import io

# Import functions from other modules
from ActualSystem.Reporting.site_report import generate_report, format_report
from ActualSystem.VectorBasedFlagging.url_processor import model as sentence_model
from ActualSystem.Classification.imitation_check import check_imitation
from ActualSystem.Classification.Color_Similarity.color_similarity import extract_colors_from_webpage, find_similar_colors
from ActualSystem.Classification.Logo_Similarity.logo_similarity import histogram_similarity

def analyze_domain(domain, url):
    results = {}

    # Generate site report
    report = generate_report(domain, url)
    results['site_report'] = format_report(report)

    # Vector-based flagging
    description_of_domain = f"{domain} website"
    domain_encoded = sentence_model.encode([description_of_domain])
    description_of_an_post = sentence_model.encode(["anpost ie the irish postal and customs agency shipping logistics postage international business"])
    similarity_with_an_post = cosine_similarity(domain_encoded, description_of_an_post)
    results['vector_similarity'] = float(similarity_with_an_post[0][0])

    # Imitation check
    domain_portions = domain.split('.')
    results['imitation_check'] = check_imitation(domain_portions)

    # Color similarity
    extracted_colors = extract_colors_from_webpage(url)
    colors_to_test = ['#FF0000', 'rgb(0, 255, 0)', 'hsl(240, 100%, 50%)']  # Example colors, replace with actual brand colors
    similar_colors = find_similar_colors(extracted_colors, colors_to_test)
    results['color_similarity'] = similar_colors

    # Logo similarity
    # Note: This part needs adjustment as we don't have the actual logo files
    # You'll need to provide paths to the target logo and the logo from the website
    # results['logo_similarity'] = histogram_similarity("path_to_target_logo.png", "path_to_website_logo.png")

    return results

# Example usage
if __name__ == "__main__":
    domain = "example.com"
    url = f"https://www.{domain}"
    results = analyze_domain(domain, url)
    print(results)