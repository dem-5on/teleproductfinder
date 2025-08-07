import logging
from .base_client import MarketplaceClient

logger = logging.getLogger(__name__)

class AmazonClient(MarketplaceClient):
    def __init__(self, region="com"):
        super().__init__("junglee/Amazon-crawler")
        self.region = region

    def _prepare_actor_input(self, search_query):
        search_url = f"https://www.amazon.{self.region}/s?k={search_query.replace(' ', '+')}"
        return {
            "categoryOrProductUrls": [{"url": search_url}],
            "maxItemsPerStartUrl": 20,
            "proxyCountry": "AUTO_SELECT_PROXY_COUNTRY",
            "maxOffers": 0,
            "scrapeSellers": False,
            "ensureLoadedProductDescriptionFields": False,
            "useCaptchaSolver": False,
            "scrapeProductVariantPrices": False,
            "scrapeProductDetails": False,
            "locationDeliverableRoutes": ["SEARCH"],
        }

    def _process_item(self, item):
        title = item.get('title', '')
        if not title:
            logger.debug("Skipping product with no title")
            return None

        # Try different price fields that Apify might return
        price = (item.get('price') or 
                item.get('currentPrice') or 
                item.get('listPrice', 'N/A'))
        
        # Try different URL fields
        url = (item.get('url') or 
              item.get('itemUrl') or 
              item.get('link', ''))
        
        if not url:
            # Construct URL if not provided
            asin = item.get('asin', '')
            if asin:
                url = f"https://www.amazon.{self.region}/dp/{asin}"
            else:
                logger.debug(f"Skipping Amazon product missing URL: {title}")
                return None

        # Process review data separately
        review_data = self._process_review_data(item)
        
        return {
            'title': title,
            'price': price,
            'url': url,
            'is_prime': item.get('isAmazonPrime') or item.get('isPrime', False),
            'asin': item.get('asin', ''),
            'marketplace': 'Amazon',
            **review_data
        }
