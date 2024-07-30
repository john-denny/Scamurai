import dns.resolver
import whois
import ssl
import socket
import builtwith
import requests

def get_dns_records(domain):
    records = {}
    try:
        records['A'] = [str(rdata) for rdata in dns.resolver.resolve(domain, 'A')]
        records['MX'] = [str(rdata.exchange) for rdata in dns.resolver.resolve(domain, 'MX')]
        records['NS'] = [str(rdata) for rdata in dns.resolver.resolve(domain, 'NS')]
        records['TXT'] = [str(rdata) for rdata in dns.resolver.resolve(domain, 'TXT')]
        records['CNAME'] = [str(rdata) for rdata in dns.resolver.resolve(domain, 'CNAME')]
    except Exception as e:
        records['error'] = str(e)
    return records

def get_whois_info(domain):
    try:
        return whois.whois(domain)
    except Exception as e:
        return {'error': str(e)}

def get_ssl_info(domain):
    ssl_info = {}
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                ssl_info['issuer'] = ssock.getpeercert()['issuer']
                ssl_info['subject'] = ssock.getpeercert()['subject']
                ssl_info['version'] = ssock.version()
                ssl_info['notBefore'] = ssock.getpeercert()['notBefore']
                ssl_info['notAfter'] = ssock.getpeercert()['notAfter']
    except Exception as e:
        ssl_info['error'] = str(e)
    return ssl_info

def get_web_server_info(url):
    try:
        response = requests.head(url)
        return response.headers.get('Server')
    except Exception as e:
        return {'error': str(e)}

def get_technology_stack(url):
    try:
        return builtwith.parse(url)
    except Exception as e:
        return {'error': str(e)}

def generate_report(domain, url):
    report = {}
    report['DNS Records'] = get_dns_records(domain)
    report['WHOIS Info'] = get_whois_info(domain)
    report['SSL Info'] = get_ssl_info(domain)
    report['Web Server'] = get_web_server_info(url)
    report['Technology Stack'] = get_technology_stack(url)
    return report

def format_report(report):
    report_text = []
    
    report_text.append("DNS Records:")
    for record_type, values in report['DNS Records'].items():
        if isinstance(values, list):
            report_text.append(f"  {record_type}:")
            for value in values:
                report_text.append(f"    - {value}")
        else:
            report_text.append(f"  {record_type}: {values}")
    
    report_text.append("\nWHOIS Info:")
    for key, value in report['WHOIS Info'].items():
        report_text.append(f"  {key}: {value}")
    
    report_text.append("\nSSL Info:")
    for key, value in report['SSL Info'].items():
        report_text.append(f"  {key}: {value}")
    
    report_text.append("\nWeb Server:")
    report_text.append(f"  {report['Web Server']}")
    
    report_text.append("\nTechnology Stack:")
    for tech_category, technologies in report['Technology Stack'].items():
        report_text.append(f"  {tech_category}:")
        for tech in technologies:
            report_text.append(f"    - {tech}")
    
    return "\n".join(report_text)

# Example usage
url = "https://www.bish.ie/"
domain = "bish.ie"
report = generate_report(domain, url)
report_text = format_report(report)
print(report_text)
