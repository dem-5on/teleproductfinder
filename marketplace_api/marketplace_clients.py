import logging
import json
from .base_client import MarketplaceClient

logger = logging.getLogger(__name__)

class TemuClient(MarketplaceClient):
    def __init__(self):
        super().__init__("LTBzVVq592mKgR6lU")

    def _prepare_actor_input(self, search_query):
        return {
            "searchQueries": [search_query],
            "maxItems": 20,
            "getReviews": True,
            "saveImages": False,  # Skip images to improve performance
            "saveVideos": False   # Skip videos to improve performance
        }

    def _process_item(self, item):
        # Debug the item structure
        logger.debug(f"Processing Temu item: {json.dumps(item, indent=2)}")
        
        # Get the title from various possible fields
        title = (item.get('title') or 
                item.get('name') or 
                item.get('productName') or
                item.get('product_name') or
                '')
                
        if not title:
            logger.debug("Skipping Temu product with no title")
            return None

        # Get price information
        price = item.get('price')
        if isinstance(price, dict):
            price = price.get('value', 'N/A')
        if not price or price == 'N/A':
            price = item.get('salePrice', {}).get('value') or item.get('originalPrice', {}).get('value')
        if price is None:
            price = 'N/A'
        else:
            price = f"${price}" if not str(price).startswith('$') else str(price)

        # Get product URL
        url = (item.get('url') or 
               item.get('productUrl') or
               item.get('link') or
               '')
               
        if not url and (product_id := (item.get('id') or item.get('productId'))):
            url = f"https://www.temu.com/product/{product_id}.html"
        
        if not url:
            logger.debug(f"Skipping Temu product missing URL: {title}")
            return None

        # Process review information
        rating = 0
        review_count = 0
        
        if isinstance(item.get('rating'), dict):
            rating = float(item['rating'].get('value', 0))
        elif isinstance(item.get('rating'), (int, float)):
            rating = float(item['rating'])
            
        if 'reviews' in item and isinstance(item['reviews'], list):
            review_count = len(item['reviews'])
        elif 'reviewsCount' in item:
            review_count = int(item['reviewsCount'])

        shipping = 'N/A'
        if 'shipping' in item:
            if isinstance(item['shipping'], dict):
                shipping = item['shipping'].get('deliveryDays', 'N/A')
            elif isinstance(item['shipping'], str):
                shipping = item['shipping']

        return {
            'title': title,
            'price': price,
            'url': url,
            'marketplace': 'Temu',
            'rating': rating,
            'review_count': review_count,
            'shipping': shipping,
            'seller': 'Temu'  # Default to Temu as seller
        }

class JumiaClient(MarketplaceClient):
    def __init__(self):
        super().__init__("easyapi/jumia-product-scraper")

    def _prepare_actor_input(self, search_query):
        return {
            "search": search_query,
            "maxProducts": 20,
            "country": "kenya"  # Can be made configurable
        }

    def _process_item(self, item):
        title = item.get('name', '')
        if not title:
            logger.debug("Skipping Jumia product with no title")
            return None

        price = item.get('price', 'N/A')
        url = item.get('url', '')

        if not url:
            logger.debug(f"Skipping Jumia product missing URL: {title}")
            return None

        review_data = self._process_review_data(item)

        return {
            'title': title,
            'price': price,
            'url': url,
            'marketplace': 'Jumia',
            **review_data
        }

class AlibabaClient(MarketplaceClient):
    def __init__(self):
        super().__init__("piotrv1001/alibaba-listings-scraper")

    def _prepare_actor_input(self, search_query):
        return {
            "search": search_query,
            "maxItems": 20,
            "minOrders": 0
        }

    def _process_item(self, item):
        title = item.get('title', '')
        if not title:
            logger.debug("Skipping Alibaba product with no title")
            return None

        # Alibaba often has price ranges
        min_price = item.get('minPrice')
        max_price = item.get('maxPrice')
        price = f"${min_price}" if min_price == max_price else f"${min_price}-${max_price}"
        
        url = item.get('detailUrl', '')

        if not url:
            logger.debug(f"Skipping Alibaba product missing URL: {title}")
            return None

        review_data = self._process_review_data(item)

        return {
            'title': title,
            'price': price,
            'url': url,
            'marketplace': 'Alibaba',
            **review_data
        }
