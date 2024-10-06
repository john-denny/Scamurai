from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_domain_similarity(domain_encoded, profile_domain):
    profile_encoded = model.encode([profile_domain])
    similarity = cosine_similarity(domain_encoded, profile_encoded)
    return float(similarity[0][0])

def compare_domains(analyzed_domain, profile_domains, threshold=0.3):
    similarities = []
    for profile_domain in profile_domains:
        similarity = get_domain_similarity(analyzed_domain, profile_domain)
        if similarity >= threshold:
            similarities.append({
                "profile_domain": profile_domain,
                "similarity": round(similarity, 2)
            })
    return sorted(similarities, key=lambda x: x["similarity"], reverse=True)