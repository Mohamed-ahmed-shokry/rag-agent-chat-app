import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

# Optional: Add other settings like ChromaDB path
VECTOR_DB_PATH = "./chroma_db"
COLLECTION_NAME = "docs_collection"