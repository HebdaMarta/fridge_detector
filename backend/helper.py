def split_products(products):

    confirmed = []
    possible = []

    for product in products:

        confidence = int(
            product["confidence"]
        )

        if confidence >= 80:
            confirmed.append(product)

        else:
            possible.append(product)

    return confirmed, possible