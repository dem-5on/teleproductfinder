import logging
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
        title = item.get('name', '')
        if not title:
            logger.debug("Skipping Temu product with no title")
            return None

        # Get price information
        original_price = item.get('originalPrice', {}).get('value')
        current_price = item.get('salePrice', {}).get('value')
        
        # Use the sale price if available, otherwise use original price
        price = current_price or original_price
        if price is None:
            price = 'N/A'
        else:
            price = f"${price}"

        # Get product URL
        url = item.get('url', '')
        if not url:
            product_id = item.get('id')
            if product_id:
                url = f"https://www.temu.com/{product_id}.html"
            else:
                logger.debug(f"Skipping Temu product missing URL: {title}")
                return None

        # Process review information
        reviews = item.get('reviews', [])
        rating = item.get('rating', {}).get('value')
        review_count = len(reviews) if reviews else item.get('reviewsCount', 0)

        return {
            'title': title,
            'price': price,
            'url': url,
            'marketplace': 'Temu',
            'rating': rating if rating is not None else 0,
            'review_count': review_count,
            'shipping': item.get('shipping', {}).get('deliveryDays', 'N/A'),
            'seller': item.get('seller', {}).get('name', 'Temu')
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
