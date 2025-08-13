from abc import ABC, abstractmethod
import logging
from apify_client import ApifyClient
import httpx

from config import settings

logger = logging.getLogger(__name__)

class MarketplaceClient(ABC):
    def __init__(self, actor_id):
        logger.debug(f"Initializing client for actor {actor_id} with token: {settings.APIFY_API_TOKEN}")
        self.client = ApifyClient(settings.APIFY_API_TOKEN)
        self.actor_id = actor_id

    @abstractmethod
    def _process_item(self, item):
        """Process a single item from the marketplace response"""
        pass

    @abstractmethod
    def _prepare_actor_input(self, search_query):
        """Prepare the input for the Apify actor"""
        pass

    def search_products(self, product_name):
        """
        Base implementation for searching products across marketplaces
        """
        try:
            # Get actor-specific input
            run_input = self._prepare_actor_input(product_name)
            
            # Run the Actor and wait for it to finish
            logger.debug(f"Starting Apify actor run for {self.actor_id}...")
            run = self.client.actor(self.actor_id).call(run_input=run_input)
            
            products = []
            logger.debug("Processing search results...")
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                try:
                    product = self._process_item(item)
                    if product:
                        products.append(product)
                except Exception as e:
                    logger.debug(f"Error processing product data: {str(e)}")
                    continue

            logger.info(f"Found {len(products)} products from {self.actor_id}")
            return products

        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {str(e)}")
            raise Exception(f"Failed to fetch products: {str(e)}")
        except Exception as e:
            logger.error(f"Error searching products: {str(e)}")
            raise Exception(f"An error occurred while searching products: {str(e)}")

    def _process_review_data(self, item):
        """
        Process review-related data from an item.
        This method can be extended later to include AI-powered review analysis.
        """
        review_data = {
            'rating': float(item.get('rating') or item.get('stars', 0) or 0),
            'reviews_count': int(item.get('reviewsCount') or item.get('numberOfReviews', 0) or 0),
            'review_analysis': None  # Placeholder for future AI analysis
        }
        return review_data
