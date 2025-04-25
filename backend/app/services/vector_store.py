import chromadb
from chromadb.utils import embedding_functions
from app.core.config import VECTOR_DB_PATH, COLLECTION_NAME, OPENAI_API_KEY

# Use OpenAI embeddings via ChromaDB's helper (or instantiate langchain_openai directly)
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=OPENAI_API_KEY,
                model_name="text-embedding-ada-002" # Or a newer model if preferred
            )

client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
# Or for in-memory: client = chromadb.Client()

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=openai_ef,
    metadata={"hnsw:space": "cosine"} # Cosine similarity is common
)

def add_documents(docs):
    """Adds LangChain documents to the collection."""
    ids = [f"doc_{i}" for i in range(len(docs))] # Simple unique IDs
    collection.add(
        ids=ids,
        documents=[doc.page_content for doc in docs],
        metadatas=[doc.metadata for doc in docs] # Store source, page etc.
    )
    print(f"Added {len(docs)} chunks to ChromaDB.")

def search_documents(query: str, n_results: int = 3):
    """Searches for relevant documents."""
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=['documents', 'metadatas'] # Include content and source info
    )
    return results # Returns dict like {'ids': [], 'documents': [], 'metadatas': []}