import base64
import json
import requests


def detect_products(image_path):

    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(
            f.read()
        ).decode("utf-8")

    prompt = """
Analyze this refrigerator image.

List every visible food product.

Estimate quantities when possible.

For each product provide:
- name
- quantity
- confidence (0-100)

Do not guess products that are not visible.

Return JSON only.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5vl:7b",
            "prompt": prompt,
            "images": [image_b64],
            "stream": False
        }
    )

    raw_response = response.json()["response"]

    raw_response = (
        raw_response
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    inventory = json.loads(raw_response)

    return inventory