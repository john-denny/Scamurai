from datetime import datetime, timedelta
import whois

def is_domain_young(domain: str) -> bool:
    # Get the age of the domain from whois
    whois_data = whois.whois(domain)
    creation_date = whois_data.creation_date
    if type(creation_date) == list:
        creation_date = creation_date[0]
    return creation_date > datetime.now() - timedelta(days=90)

