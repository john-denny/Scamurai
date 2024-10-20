from datetime import datetime, timedelta
import whois

def whois_data(domain: str) -> tuple:
    # Get the age of the domain from whois
    whois_data = whois.whois(domain)
    
    # Check if whois_data is None
    if whois_data is None:
        return False, None, None  # Return null-proof values

    creation_date = whois_data.creation_date
    
    # Check if creation_date is None
    if creation_date is None:
        return False, whois_data.get("emails"), whois_data.get("name_servers")

    if type(creation_date) == list:
        creation_date = creation_date[0]
    
    nameserver = whois_data.nameservers if whois_data.nameservers else None  # Get the nameserver safely

    return creation_date > datetime.now() - timedelta(days=90), whois_data.get("emails"), whois_data.get("name_servers")

