from pinecone import Pinecone
import json
import uuid
import os

pc = Pinecone(api_key = os.environ.get("PINECONE_API_KEY"))

index = pc.Index("voicecaretest3")
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
        metadata = [
            str("user_id :" + str(user_id)),
            str("category:" + str(category))
            ##**{k: str(v) if isinstance(v, (int, float, dict, list)) else v for k, v in details.items()}
        ]

        records.append({"_id": record_id, "chunk_text": text_data, "metadata": metadata})

    index.upsert_records(namespace = user_id, records = records)
    print(f"Data for User {user_id} inserted into Pinecone.")

