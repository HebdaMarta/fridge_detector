from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form
)
from backend.schemas import RecipeGenerationRequest
from backend.rag import search_recipe
from backend.llm import generate_recipe
from pathlib import Path
from backend.detector import detect_products
from backend.helper import split_products

app = FastAPI()


@app.post("/recipe")
async def recipe(
    image: UploadFile = File(...),
    preference: str = Form(default="")
):
    path = f"data/uploads/{image.filename}"

    Path("data/uploads").mkdir(
        parents=True,
        exist_ok=True
    )

    with open(path, "wb") as f:
        f.write(await image.read())

    inventory = detect_products(path)

    print("\nINVENTORY:")
    print(inventory)
    print(type(inventory))

    if not isinstance(inventory, dict):
        return {
            "error": "Inventory is not a dict",
            "inventory": str(inventory)
        }

    if "products" not in inventory:
        return {
            "error": "Missing products key",
            "inventory": inventory
        }

    products = (
            inventory.get("products")
            or inventory.get("fridge_contents")
            or []
    )

    confirmed_products, possible_products = split_products(
        products
    )

    return {
        "confirmed_products": confirmed_products,
        "possible_products": possible_products
    }

@app.post("/generate_recipes")
async def generate_recipes(
    request: RecipeGenerationRequest
):

    recipes = search_recipe(
        request.products,
        request.preference
    )

    answer = generate_recipe(
        request.products,
        recipes,
        request.preference
    )

    return answer