from pinecone import Pinecone
import json
import uuid
import os
from embeddings import create_embeddings
pc = Pinecone(api_key = os.environ.get("PINECONE_API_KEY"))
index = pc.Index("voicecare5")
def insert_data(data_json):
    data = data_json  # No need to load again if it's already a dict
    user_id = data['user_id']

    categories = {
        "basic_info" : data["basic_info"],
        "medical_info" : data["medical_info"],
        "daily_routine" : data["daily_routine"],
        "emergency_protocol" : data["emergency_protocol"],
    }

    records = []

    for category, details in categories.items():
        record_id = str(uuid.uuid4())
        text_data = " ".join(f"{k}: {v}" for k, v in details.items())  # Convert dict to text.
        metadata = {
            "user_id" : str(user_id),
            "category": str(category),
            "content": str(details)
            ##**{k: str(v) if isinstance(v, (int, float, dict, list)) else v for k, v in details.items()}
        }

        records.append({"id": record_id, "values": create_embeddings(json.dumps(details, indent=2)), "metadata": metadata})
    index.upsert(namespace = user_id, vectors=records)
    print(f"Data for User {user_id} inserted into Pinecone.")

