import builtwith
from datetime import datetime
import os
import shutil
import requests

def save_report(results, url, company_name):
    # Create a directory for the report with the url (Modify the url to be safe and move the tld to the end of the folder name)
    safe_url = url.replace("http://", "").replace("https://", "")
    safe_url = safe_url.replace("/", "_")
    safe_url = safe_url.replace(":", "_")
    # Add the date to the folder name
    safe_url = safe_url + "_" + datetime.now().strftime("%Y-%m-%d")

    # Make the directory
    os.makedirs(safe_url, exist_ok=True)

    # Create a subdirectory called logos
    os.makedirs(os.path.join(safe_url, "logos"), exist_ok=True)
    
    # Move the logos from the temp directory to the actual logo directory
    if results['logo_similarity']:
        for logo_path, similarity in results['logo_similarity'].items():
            try:
                if os.path.exists(logo_path):
                    logo_filename = os.path.join(safe_url, "logos", os.path.basename(logo_path))
                    shutil.move(logo_path, logo_filename)
                    print(f"Moved logo: {logo_filename}")
                else:
                    print(f"Logo file not found: {logo_path}")
            except Exception as e:
                print(f"Error moving logo from {logo_path}: {str(e)}")

    # Create a markdown file called report.md
    with open(os.path.join(safe_url, "report.md"), "w") as f:
        f.write(f"# {url} Report\n\n")
        f.write(f"## Domain Compared against: {company_name}\n\n")

        # Add all the results to the report
        for key, value in results.items():
            formatted_key = ' '.join(word.capitalize() for word in key.replace('_', ' ').split())
            f.write(f"### {formatted_key}\n\n")
            f.write(f"{value}\n\n")
    
        # The sites infrastructure
        f.write("## Sites Infrastructure\n\n")
        f.write(str(builtwith.builtwith(url)))


    print(f"Report saved in: {safe_url}")
