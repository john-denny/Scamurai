from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def analyze_domain(domain):
    domain_name = domain.split('.')[0]
    domain_encoded = model.encode([domain_name])
    return domain_encoded

def get_domain_similarity(domain_encoded, company_description):
    company_encoded = model.encode([company_description])
    similarity = cosine_similarity(domain_encoded, company_encoded)
    return float(similarity[0][0])