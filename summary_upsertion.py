from pinecone import Pinecone
import json
import uuid
from embeddings import create_embeddings
import os
from dotenv import load_dotenv
from messaging import send_message

load_dotenv()
pc = Pinecone(api_key = os.environ.get("PINECONE_API_KEY"))

index = pc.Index("voicecare5")

def summary_upsert(username, summary):
    if not summary or summary.strip() == "NO_SUMMARY":
        return
    record_id = str(uuid.uuid4())
    metadata = {
        "user_id" : username,
        "content" : summary,
        "type" : "summary"
    }
    
    records = [{"id": record_id, "values": create_embeddings(json.dumps(summary, indent=2)), "metadata": metadata}]
    index.upsert(namespace = username, vectors=records)
    send_message(summary, '+919166619120')
    print(f"Summary for User {username} inserted into Pinecone.")