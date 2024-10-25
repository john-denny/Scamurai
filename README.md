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
  - CairoSVG has dependencies which may depend on your Operating System. On Ubuntu Install `libcairo2 python3-dev libffi-dev ffmpeg libsm6 libxext6 ` using the apt.

## Trelis
Built as part of a [Trelis Grant](https://trelis.com/trelis-ai-grants/)
