import logging
from .base_client import MarketplaceClient

logger = logging.getLogger(__name__)

class TemuClient(MarketplaceClient):
    def __init__(self):
        super().__init__("amit123/temu-products-scraper")

    def _prepare_actor_input(self, search_query):
        return {
            "searchQueries": [search_query],
            "maxProducts": 20
        }

    def _process_item(self, item):
        title = item.get('title', '')
        if not title:
            logger.debug("Skipping Temu product with no title")
            return None

        price = item.get('price', 'N/A')
        url = item.get('productUrl', '')

        if not url:
            logger.debug(f"Skipping Temu product missing URL: {title}")
            return None

        review_data = self._process_review_data(item)

        return {
            'title': title,
            'price': price,
            'url': url,
            'marketplace': 'Temu',
            **review_data
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
