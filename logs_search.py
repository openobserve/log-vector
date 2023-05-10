import json
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer

encoder = SentenceTransformer('all-MiniLM-L6-v2') # Model to create embeddings

qdrant = QdrantClient(path="./qdrant_storage")  # Create persistent Qdrant instance


# Let's now search for something

hits = qdrant.search(
    collection_name="logs",
    query_vector=encoder.encode("error denied").tolist(),
    limit=3
)
for hit in hits:
  print(json.dumps(hit.payload["log"], indent=4), "score:", hit.score)

