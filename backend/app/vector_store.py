import chromadb
from chromadb.utils import embedding_functions

CHROMA_PATH = "./chroma_data"
COLLECTION_NAME = "notes"

embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function
)

def add_note(note_id: int, text: str, user_id: int):
    collection.upsert(
        documents=[text],
        ids=[str(note_id)],
        metadatas=[{"user_id": user_id}]
    )

def delete_note(note_id: int):
    collection.delete(ids=[str(note_id)])

def search_notes(query: str, user_id: int, n_results: int = 5) -> list[str]:
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where={"user_id": user_id}
    )
    return results["documents"][0] if results["documents"] else []