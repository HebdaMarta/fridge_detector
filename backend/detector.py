import base64
import json
import requests
from PIL import Image
from io import BytesIO


def detect_products(image_path):
    print(f"\n[DETECTOR] 1. Otwieranie obrazu: {image_path}", flush=True)

    try:
        with Image.open(image_path) as img:
            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=85)
            image_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        print("[DETECTOR] Obraz zakodowany. Wysyłam do AI...", flush=True)
    except Exception as e:
        print(f"[DETECTOR ERROR] Błąd przetwarzania obrazu: {e}", flush=True)
        return {"products": []}

    prompt = """
    List the food items visible in this image.
    Return ONLY a valid JSON array. Do not write any other text.
    Format exactly like this:
    [{"name": "apple", "quantity": "1", "confidence": 95}, {"name": "milk", "quantity": "1", "confidence": 90}]
    """

    print("[DETECTOR] 2. qwen2.5vl:7b w akcji", flush=True)

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5vl:7b",
                "prompt": prompt,
                "images": [image_b64],
                "stream": False
            },
            timeout=50000
        )
        response.raise_for_status()
    except Exception as e:
        print(f"[DETECTOR ERROR] Błąd połączenia z Qwen: {e}", flush=True)
        return {"products": []}

    print("[DETECTOR] 3. qwen2.5vl:7b działa, czyścimy", flush=True)
    raw_response = response.json().get("response", "")

    clean_response = raw_response.strip()

    if clean_response.startswith("```json"):
        clean_response = clean_response[7:]
    elif clean_response.startswith("```"):
        clean_response = clean_response[3:]

    if clean_response.endswith("```"):
        clean_response = clean_response[:-3]

    clean_response = clean_response.strip()

    if clean_response.endswith("]") and not clean_response.startswith("{"):
        pass
    elif clean_response.endswith("]") and clean_response.startswith("{"):
        clean_response += "}"

    try:
        inventory = json.loads(clean_response)

        if isinstance(inventory, list):
            inventory = {"products": inventory}
        elif "fridge_contents" in inventory:
            inventory = {"products": inventory["fridge_contents"]}
        elif "products" not in inventory:
            inventory = {"products": []}

        for prod in inventory["products"]:
            if "quantity" not in prod:
                prod["quantity"] = "1"
            if "confidence" not in prod:
                prod["confidence"] = 50

        print(f"[DETECTOR] 4. Zrobione. Znaleziono {len(inventory['products'])} produktów.", flush=True)
        return inventory

    except json.JSONDecodeError as e:
        print(f"[DETECTOR ERROR] Błąd sparsowania odpowiedzi: {e}", flush=True)
        print(f"--- Odpowiedź Qwen \n{raw_response}\n", flush=True)
        return {"products": []}