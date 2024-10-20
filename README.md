# Scamurai 
A multi-factor method of detecting phishing and brand impersonation sites, then logging them in a report

## Current Factors Compared against
- Dominant Color Similarity - Using the `L*a*b` Colorset 
- Domain Cosine similarity - How similar a potential phishing domain is to a legitimate one using word embeddings
- Some whois information - such as age
- Logo comparison - Compares Logos which appear on a site to those of a site's profile

## Profile Generation
- Profiles can be found in `/src/config/company_profiles.py`
- Then add logos and images to the logos directory which you specify

# Dependencies & Setup
- Use pip to install the requirements file
- [CairoSVG is used for scraped SVGs from sites for logo similarity & comparison](https://cairosvg.org/)


## Trelis
Built as part of a [Trelis Grant](https://trelis.com/trelis-ai-grants/)
