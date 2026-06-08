import requests

OLLAMA_URL = (
    "http://localhost:11434/api/generate"
)

def generate_recipe(
        products,
        recipes,
        preference
):

    prompt = f"""
    Products:
    {products}

    User preference:
    {preference}

    Recipes:
    {recipes}

    Choose best recipe.
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "phi3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]