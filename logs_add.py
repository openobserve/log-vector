import json
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer

encoder = SentenceTransformer('all-MiniLM-L6-v2')  # Model to create embeddings


# Open the JSON file
with open('k8slog_json.json') as f:
    logs = json.load(f)

logs = [log for log in logs if 'log' in log]


# qdrant = QdrantClient(
#     url="https://e2a3ccfc-46f8-42a8-885a-a8561c994726.us-east-1-0.aws.cloud.qdrant.io:6333",
#     api_key="pWcZK87BnIOrmOc3UEAcFInctHwb46HNqasDF6D8Y1FAsF9BNcsVoQ",
# )
qdrant = QdrantClient(path="./qdrant_storage")  # Create persistent Qdrant instance

filtered_logs = []
for logline in logs:
    if logline['log'] is not None:
        filtered_logs.append(logline)

filtered_messages = []
for logline in logs:
    if logline['log'] is None:
        filtered_messages.append(logline)

# Create collection to store logs
qdrant.recreate_collection(
    collection_name="logs",
    vectors_config=models.VectorParams(
        # Vector size is defined by used model
        size=encoder.get_sentence_embedding_dimension(),
        distance=models.Distance.COSINE
    )
)

# # Let's vectorize descriptions and upload to qdrant

qdrant.upload_records(
    collection_name="logs",
    records=[
        models.Record(
            id=idx,
            vector=encoder.encode(logline['log']).tolist(),
            payload=logline
        ) for idx, logline in enumerate(filtered_logs)
    ]
)

qdrant.upload_records(
    collection_name="logs",
    records=[
        models.Record(
            id=idx,
            vector=encoder.encode(logline['message']).tolist(),
            payload=logline
        ) for idx, logline in enumerate(filtered_messages)
    ]
)
