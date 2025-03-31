from pinecone import Pinecone
import json
import uuid
import os

pc = Pinecone(api_key = os.environ.get("PINECONE_API_KEY"))

index = pc.Index("voicecaretest3")

def summary_upsert(username, summary):
    if not summary or summary.strip() == "NO_SUMMARY":
        return
    record_id = str(uuid.uuid4())
    metadata = [
        str("user_id :" + str(username)),
        str("category:" + "summary")
    ]
    
    records = [{"_id": record_id, "chunk_text": summary, "metadata": metadata}]
    index.upsert_records(namespace = username, records = records)
    print(record_id)
    print(f"Summary for User {username} inserted into Pinecone.")


    
