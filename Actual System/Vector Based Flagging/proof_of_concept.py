from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

# Two lists of sentences
sentences1 = [
    "vodafone ie com ireland an online phone carrier provider",
    "anpost ie the irish postal and customs agency",
    "A man is playing guitar",
    "I drink soy milk everyday",
    "Get rich quickly"
]

sentences2 = [
    "vodafone terms ie com",
    "customs postal info",
    "A woman watches TV",
    "I own twitter premium",
    "dhl", 
]


# Compute embeddings for both lists
embeddings1 = model.encode(sentences1)
embeddings2 = model.encode(sentences2)

# Compute cosine similarities
similarities = model.similarity(embeddings1, embeddings2)

# Output the pairs with their score
for idx_i, sentence1 in enumerate(sentences1):
    print(sentence1)
    for idx_j, sentence2 in enumerate(sentences2):
        print(f" - {sentence2: <30}: {similarities[idx_i][idx_j]:.4f}")