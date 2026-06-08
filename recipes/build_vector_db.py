from pathlib import Path
import json
import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_PATH = BASE_DIR / "data" / "chroma"

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = client.get_or_create_collection(
    "recipes"
)

with open("recipes/recipes.json", encoding="utf-8") as f:
    recipes = json.load(f)

for idx, recipe in enumerate(recipes):

    text = (
        recipe["title"]
        + " "
        + " ".join(recipe["ingredients"])
    )

    emb = model.encode(text)

    collection.add(
        ids=[str(idx)],
        embeddings=[emb.tolist()],
        documents=[json.dumps(recipe)]
    )

print("Documents in collection:")
print(collection.count())