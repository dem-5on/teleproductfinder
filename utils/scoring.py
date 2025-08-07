def extract_price(price_str):
    """
    Extracts numerical price from a string like '$123.45' or '123,45 €'
    """
    if not price_str or not isinstance(price_str, str):
        return float('inf')
    
    # Remove currency symbols and common separators
    price_str = price_str.replace('$', '').replace('€', '').replace('£', '')
    price_str = price_str.replace(',', '').replace(' ', '')
    
    try:
        return float(price_str)
    except (ValueError, TypeError):
        return float('inf')

def calculate_score(product):
    """
    Calculates a score for a product based on its rating, number of reviews, and price.
    """
    # Get rating (0-5 scale)
    rating = float(product.get('stars', 0) or 0)
    
    # Get number of reviews
    reviews = int(product.get('reviewsCount', 0) or 0)
    
    # Get price as a number
    price_str = product.get('price', '')
    price = extract_price(price_str)

    # Normalize scores
    rating_score = rating / 5.0  # Normalize rating to 0-1
    reviews_score = min(reviews / 1000.0, 1.0)  # Normalize reviews, cap at 1000
    price_score = 1000.0 / (price + 1000.0)  # Price score closer to 1 for lower prices

    # Combine scores with weights
    # 50% rating, 30% price, 20% reviews
    score = (rating_score * 0.5) + (price_score * 0.3) + (reviews_score * 0.2)

    return score
