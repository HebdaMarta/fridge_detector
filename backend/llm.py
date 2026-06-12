import requests
import json

OLLAMA_URL = (
    "http://localhost:11434/api/generate"
)

def generate_recipe(
        products,
        recipes,
        preference
):
    prompt = f"""
    You are a professional chef.

    Available ingredients:
    {products}

    User preference:
    {preference}

    Retrieved recipes:
    {recipes}

    Create 3 recipe suggestions.

    Return JSON only.

    Example:

    {{
      "recipes": [
        {{
          "title": "Vegetable Omelette",
          "description": "Healthy omelette with vegetables",
          "time": "15 min",
          "difficulty": "easy"
        }},
        {{
          "title": "Tomato Salad",
          "description": "Fresh salad",
          "time": "10 min",
          "difficulty": "easy"
        }},
        {{
          "title": "Vegetable Bowl",
          "description": "Warm vegetable bowl",
          "time": "20 min",
          "difficulty": "medium"
        }}
      ]
    }}
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "phi3",
            "prompt": prompt,
            "stream": False
        }
    )

    raw = response.json()["response"]

    raw = (
        raw
            .replace("```json", "")
            .replace("```", "")
            .strip()
    )

    print(raw)

    return json.loads(raw)