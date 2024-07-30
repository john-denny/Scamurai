import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def check_imitation(domain_portions:list[2]) -> bool:
    """Checks if a site is imitation"""
    domain_to_check = f"https://www.{domain_portions[0]}.{domain_portions[1]}/"

    site_html = get_page_content(domain_to_check)
    asset_urls = extract_assets(domain_to_check, site_html)

    # Pull down all images from site and save them to temp
    for url in asset_urls["images"]:
        file_path = "images/"+url.rpartition("/")[2]

        response = requests.get(url)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        
    # TODO Process the images

    # TODO Delete all images


def get_page_content(url):
    """Fetches the Html Contents of a page or Raises a ``HTTPError``"""
    response = requests.get(url)
    response.raise_for_status()
    return response.text

# Parse the url
def extract_assets(url, html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    assets_dict = {
        'images': set(),
        'scripts': set(),
        'stylesheets': set()
    }

    # Extract images
    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            assets_dict['images'].add(urljoin(url, src))

    # Extract scripts
    for script in soup.find_all('script'):
        src = script.get('src')
        if src:
            assets_dict['scripts'].add(urljoin(url, src))

    # Extract stylesheets
    for link in soup.find_all('link', rel='stylesheet'):
        href = link.get('href')
        if href:
            assets_dict['stylesheets'].add(urljoin(url, href))

    return assets_dict



check_imitation(["google","com"])