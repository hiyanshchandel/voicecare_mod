from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))
def create_embeddings(text):
    embedding = client.embeddings.create(
    model=os.environ.get("EMBEDDING_MODEL_OPENAI"),
    input=text,
    encoding_format="float"
    )
    return embedding.data[0].embedding
