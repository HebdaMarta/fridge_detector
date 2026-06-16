#import os
#os.environ["CUDA_VISIBLE_DEVICES"] = "" # w przypadku problemu ze sterownikiem GPU takie cuś
from sqlalchemy.orm import Session
from sqlalchemy import select, Engine, cast, String
from typing import Optional, List
from sentence_transformers import SentenceTransformer
from sql_engine_embedding import engine
from main_embedding import Recipes

print("[LOG 1] Ładowanie modelu", flush=True)
model = SentenceTransformer("distiluse-base-multilingual-cased-v2")
print("[LOG 2] Model załadowany", flush=True)

def find_recipes(
        engine: Engine,
        search_text: str, #tutaj coś użytkownik może wpisać sobie, np. "mam ochotę na coś lekkiego z ryby"
        ingredients_count: Optional[int] = None,
        fridge_ingredients: Optional[List[str]] = None,
        max_kcal: Optional[int] = None, #limit kalorii
        ):
    ingredients_str = ", ".join(fridge_ingredients)
    combined_query_text = f"{search_text}. Mam w lodówce: {ingredients_str}."
    print("[LOG 4] Jestem w funkcji find_recipes. Generuję wektor zapytania", flush=True)
    query_embedding = model.encode(combined_query_text).tolist()
    print("[LOG 5] Wektor wygenerowany pomyślnie", flush=True)

    with Session(engine) as session:
        query = select(Recipes)
        if ingredients_count:
            query = query.filter(Recipes.ingredient_count <= ingredients_count)

        if max_kcal:
            query = query.filter(Recipes.kcal <= max_kcal)

        #ważne: szukamy przepisu po dostępnych składnikach z modelu CV
        #if fridge_ingredients:
         #   cleaned_fridge = [i.lower().strip() for i in fridge_ingredients]
          #  query = query.filter(Recipes.ingredients.contained_by(cleaned_fridge))

        query = query.order_by(
            Recipes.recipe_embedding.cosine_distance(query_embedding)
        ).limit(3)

        print("[LOG 6] Wysyłam zapytanie do bazy SQL", flush=True)
        result = session.execute(query, execution_options={"prebuffer_rows": True})
        recipes = result.scalars().all() #.first() zwróciłoby 1 najlepszy przepis
        print(f"[LOG 7] Baza danych zwróciła wyników: {len(recipes)}", flush=True)
        return recipes

print("[LOG 3] Wywołuję funkcję wyszukiwania przepisów", flush=True)
przepis_z_lodowki = find_recipes(
    engine,
    search_text="chciałbym coś lekkiego i niskokalorycznego",
    ingredients_count=7,
    fridge_ingredients=["eggs", "cream"],
    max_kcal=5500
)

print("[LOG 8] Przechodzę do bloku wyświetlania wyników", flush=True)
if przepis_z_lodowki:
    for numer, przepis in enumerate(przepis_z_lodowki, 1):
        print(f" ZNALAZŁEM PRZEPYSZCZNE DANIA DLA CIEBIE")
        print(f"Nazwa: {przepis.name}")
        print(f"Liczba składników w przepisie: {przepis.ingredient_count}")
        print(f"Wszystkie składniki: {przepis.ingredients}")
        print(f"\nKroki do wykonania:\n{przepis.steps}")
else:
    print("Ziom, w tej lodówce nic nie ma!")