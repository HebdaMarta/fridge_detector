import json
import os
from sql_engine_embedding import engine
from main_embedding import Base, Recipes
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session
from sqlalchemy import text


JSON_PATH = os.path.join('data', 'recipes.json')
if not os.path.exists(JSON_PATH):
    print(f"Nie ma pliku json w ścieżce: {JSON_PATH}")
    exit(1)

Base.metadata.drop_all(engine)

with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    conn.commit()

Base.metadata.create_all(engine)

checkpoint = "distiluse-base-multilingual-cased-v2"
model = SentenceTransformer(checkpoint)

def parse_nutrient(value: str) -> float | None:
    if not value:
        return None
    clean_value = str(value).lower().replace("g", "").strip()
    try:
        return float(clean_value)
    except ValueError:
        return None
#ładuję jsona
with open(JSON_PATH, "r", encoding="utf-8") as f:
    recipes_data = json.load(f)[:1000]
print(f"wczytano JSON")

with Session(engine) as session:
    for i, item in enumerate(recipes_data):

        """PREPROCESSING JSONA"""
        nutrients = item.get("nutrients", {})

        kcal_val = nutrients.get("kcal")
        kcal_int = parse_nutrient(nutrients.get("kcal"))
        if kcal_int is not None:
            kcal_int = int(kcal_int)

        protein_val = parse_nutrient(nutrients.get("protein"))
        fat_val = parse_nutrient(nutrients.get("fat"))
        carbs_val = parse_nutrient(nutrients.get("carbs"))

        #Context enrichment dla modelu AI
        diet_tags = ""
        if kcal_int and kcal_int <= 400:
            diet_tags = "Danie jest niskokaloryczne, dietetyczne, fit, lekkie"

        #Sentence Transformer potrzebuje tekstu, listy nie zrozumie
        ingredients_list = item.get("ingredients", [])
        steps_list = item.get("steps", [])

        ingredients_str = ", ".join(ingredients_list)
        steps_str = " ".join(steps_list)

        full_context = (
            f"Nazwa dania: {item.get('name')}. "
            f"Opis dania: {item.get('description')}. "
            f"Wartość energetyczna to {kcal_int} kcal. {diet_tags} "
            f"Potrzebne składniki: {ingredients_str}. "
            f"Przepis na danie: {steps_str}"
        )
        print(f"Leci przepis {i + 1}: {item.get('name')}...", end="", flush=True)
        embedding = model.encode(full_context).tolist()
        ingredient_count_val = len(ingredients_list)

        recipe = Recipes(
            id=item.get("id"),
            #url=item.get("url"),
            #image=item.get("image"),
            name=item.get("name"),
            description=item.get("description"),
            #author=item.get("author"),
            #ratings=item.get("rattings", 0),
            ingredients=ingredients_list,
            steps=steps_list,
            kcal=kcal_int,
            #protein=protein_val,
            #fat=fat_val,
            #carbs=carbs_val,
            difficulty=item.get("difficult"),
            subcategory=item.get("subcategory"),
            dish_type=item.get("dish_type"),
            ingredient_count=ingredient_count_val,
            recipe_embedding=embedding
        )
        session.add(recipe)
    session.commit()
print("Zrobiłem bazę danych")