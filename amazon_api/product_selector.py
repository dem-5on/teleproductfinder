from utils.scoring import calculate_score

def select_best_deal(products):
    """
    Selects the best deal from a list of products.
    """
    if not products:
        return None

    # Filter out products without essential information
    valid_products = [
        p for p in products 
        if p.get('title') and p.get('price') and p.get('url')
    ]

    if not valid_products:
        return None

    try:
        best_product = max(valid_products, key=calculate_score)
        return best_product
    except Exception as e:
        print(f"Error selecting best deal: {str(e)}")
        # If scoring fails, return the first valid product
        return valid_products[0] if valid_products else None
