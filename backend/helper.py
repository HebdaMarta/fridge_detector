def split_products(products):

    confirmed = []
    possible = []

    for product in products:

        if product["confidence"] >= 80:
            confirmed.append(product)

        else:
            possible.append(product)

    return confirmed, possible