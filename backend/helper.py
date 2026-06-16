def split_products(products):
    confirmed = []
    possible = []

    for product in products:
        raw_confidence = product.get("confidence", 0)
        try:
            if isinstance(raw_confidence, str):
                raw_confidence = raw_confidence.replace("%", "").strip()
            confidence = int(float(raw_confidence))

        except (ValueError, TypeError):
            print(
                f"Warning: Niska pewność: '{raw_confidence}' dla produktu: {product.get('name', 'Nieznany')}",
                flush=True)
            confidence = 0
        if confidence >= 80:
            confirmed.append(product)
        else:
            possible.append(product)

    return confirmed, possible