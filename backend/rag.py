import chromadb
from pathlib import Path
from sentence_transformers import (
    SentenceTransformer
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_PATH = BASE_DIR / "data" / "chroma"

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = client.get_or_create_collection(
    "recipes"
)

def search_recipe(
        products,
        preference
):

    query = (
        " ".join(products)
        + " "
        + preference
    )

    embedding = model.encode(query)

    result = collection.query(
        query_embeddings=[
            embedding.tolist()
        ],
        n_results=3
    )

    return result