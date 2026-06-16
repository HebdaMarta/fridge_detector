from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy import select
from sentence_transformers import SentenceTransformer

from backend.schemas import RecipeGenerationRequest
from backend.detector import detect_products
from backend.helper import split_products
from backend.sql_engine_embedding import engine
from backend.main_embedding import Recipes
app = FastAPI()

print("[API] Ładowanie modelu embeddingów distiluse...", flush=True)
model_embed = SentenceTransformer("distiluse-base-multilingual-cased-v2")
print("[API] Model distiluse gotowy do obsługi wyszukiwań!", flush=True)


@app.post("/recipe")
async def recipe(
        image: UploadFile = File(...),
        preference: str = Form(default="")
):
    path = f"data/uploads/{image.filename}"
    Path("data/uploads").mkdir(parents=True, exist_ok=True)

    with open(path, "wb") as f:
        f.write(await image.read())

    inventory = detect_products(path)

    products = inventory.get("products") or []
    confirmed_products, possible_products = split_products(products)

    return {
        "confirmed_products": confirmed_products,
        "possible_products": possible_products
    }

@app.post("/generate_recipes")
async def generate_recipes(request: RecipeGenerationRequest):
    try:
        ingredients_str = ", ".join(request.products)
        combined_query_text = f"{request.preference}. Mam w lodówce: {ingredients_str}."

        print(f"[API] Szukam przepisów dla frazy: '{combined_query_text}'")
        query_embedding = model_embed.encode(combined_query_text).tolist()

        with Session(engine) as session:
            query = (
                select(Recipes)
                .order_by(Recipes.recipe_embedding.cosine_distance(query_embedding))
                .limit(3)
            )
            result = session.execute(query)
            db_recipes = result.scalars().all()

        formatted_recipes = []
        for r in db_recipes:
            steps_formatted = "\n\n".join([f"{idx + 1}. {step}" for idx, step in enumerate(r.steps)])

            description_text = (
                f"📊 Calories: {r.kcal or 'No information'} kcal\n\n"
                f"🛒 Ingredients: {', '.join(r.ingredients)}\n\n"
                f"📝 Recipe steps:\n{steps_formatted}"
            )

            formatted_recipes.append({
                "title": r.name,
                "description": description_text,
                "time": f"Ingredient count: {r.ingredient_count}",
                "difficulty": r.difficulty or "Medium"
            })
        return {"recipes": formatted_recipes}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))