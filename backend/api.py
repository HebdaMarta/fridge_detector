from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form
)

from backend.detector import detect_products
from backend.rag import search_recipe
from backend.llm import generate_recipe
from pathlib import Path
from backend.helper import split_products

app = FastAPI()

@app.post("/recipe")
async def recipe(
    image: UploadFile = File(...),
    preference: str = Form(...)
):
    path = f"data/uploads/{image.filename}"

    Path("data/uploads").mkdir(
        parents=True,
        exist_ok=True
    )

    with open(path, "wb") as f:
        f.write(await image.read())

    inventory = detect_products(path)

    print(inventory)

    confirmed_products, possible_products = split_products(
        inventory["products"]
    )

    return {
        "confirmed_products": confirmed_products,
        "possible_products": possible_products
    }