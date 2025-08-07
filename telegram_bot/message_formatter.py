def format_product_message(product):
    """
    Formats the product information into a user-friendly message.
    """
    if not product:
        return "❌ **No products found!** Please try a different search term."

    rating_stars = "⭐" * int(product.get('rating', 0)) if product.get('rating') else "N/A"
    reviews = f"({product['reviews_count']} reviews)" if product.get('reviews_count') else ""

    return f"""✅ **Best Deal Found!**
**Product:** {product['title']}
**Price:** {product['price']}
**Rating:** {rating_stars} {reviews}
**Link:** {product['url']}
"""