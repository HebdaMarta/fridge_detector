from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form
)

from pathlib import Path

from backend.detector import detect_products
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

    confirmed_products, possible_products = split_products(
        inventory["products"]
    )

    return {
        "confirmed_products": confirmed_products,
        "possible_products": possible_products
    }