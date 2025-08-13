def escape_markdown(text):
    """Helper function to escape telegram markdown symbols"""
    if text is None:
        return ""
    
    # Complete list including missing characters
    escape_chars = '_*[]()~`><#+-=|{}.!\\'
    
    text = str(text)
    # Escape backslashes first to avoid double-escaping
    text = text.replace('\\', '\\\\')
    
    # Then escape other characters
    for char in '_*[]()~`><#+-=|{}.!':
        text = text.replace(char, '\\' + char)
    
    return text
    
def format_product_message(product):
    """
    Formats the product information into a user-friendly message.
    """
    if not product:
        return "❌ **No products found!** Please try a different search term."

    rating_stars = "⭐" * int(float(product.get('rating', 0))) if product.get('rating') else "N/A"
    reviews = f"({product.get('reviews_count', '')} reviews)" if product.get('reviews_count') else ""
    
    title = escape_markdown(product['title'])
    url = product['url']

    message = f"""✅ **Best Deal Found!**
**Product:** {title}
**Price:** {product['price']}
**Rating:** {rating_stars} {reviews}
"""
    return message, url