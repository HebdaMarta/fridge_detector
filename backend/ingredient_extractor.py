import requests
import json


def extract_ingredients(caption):

    prompt = f"""
You are a food recognition assistant.

Extract all food ingredients mentioned in the text.

Ignore:
- refrigerator
- boxes
- bottles
- microwave
- containers

Return ONLY JSON.

Example:

{{
    "ingredients": [
        "tomatoes",
        "eggs",
        "capsicum"
    ]
}}

Text:

{caption}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma3:4b",
            "prompt": prompt,
            "stream": False
        }
    )

    text = response.json()["response"]
    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    data = json.loads(text)

    return data["ingredients"]