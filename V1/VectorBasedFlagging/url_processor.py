
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the model
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Language Model Loaded!")

# Load the dataframe
df = pd.read_csv("sample.csv")
print("Data Loaded!")

# Initialise the list of domains to scan
suspicious_domains = []

# Break each domain up into its components (domain, tld)
domain_names_clean = [i.partition(".")[0:2:2] for i in df["domainName"]]

# Description encoding
description_of_an_post = model.encode(["anpost ie the irish postal and customs agency shipping logistics postage international business"])

# Monitor encoding and similarity computation
for i, domain_name in enumerate(domain_names_clean):
    current_domain_encoded = model.encode([domain_name[0]])
    
    # Calculate similarity
    similarity_with_an_post = cosine_similarity(current_domain_encoded, description_of_an_post)
    
    # Check if similarity exceeds the threshold
    if float(similarity_with_an_post[0][0]) > 0.4:
        print(f"Domain: {domain_name} \nSimilarity: {similarity_with_an_post[0][0]}")
        suspicious_domains.append(domain_name)
    
    # Print progress for every 1000 domains processed
    if i % 1000 == 0:
        print(f"Number of Domains processed: {i}")

print(f"Suspicious Domains: {suspicious_domains}")
