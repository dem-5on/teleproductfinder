from typing import List, Dict, Any
import logging
from .amazon_client import AmazonClient
from .marketplace_clients import TemuClient, JumiaClient, AlibabaClient, AliExpressClient

logger = logging.getLogger(__name__)

class MarketplaceManager:
    MARKETPLACE_NAMES = {
        'amazon': 'Amazon',
        'temu': 'Temu',
        'jumia': 'Jumia',
        'alibaba': 'Alibaba',
        'aliexpress': 'AliExpress'
    }

    def __init__(self):
        self.clients = {
            'amazon': AmazonClient(),
            'temu': TemuClient(),
            'jumia': JumiaClient(),
            'alibaba': AlibabaClient(),
            'aliexpress': AliExpressClient()
        }
    
    def get_available_marketplaces(self):
        """Returns a list of available marketplace identifiers"""
        return list(self.clients.keys())
    
    def get_marketplace_display_name(self, marketplace: str) -> str:
        """Get the display name for a marketplace"""
        return self.MARKETPLACE_NAMES.get(marketplace, marketplace.title())

    def search_marketplace(self, marketplace: str, product_name: str, region: str = None) -> List[Dict[str, Any]]:
        """
        Search for products in a specific marketplace
        
        Args:
            marketplace (str): The marketplace identifier ('amazon', 'temu', etc.)
            product_name (str): The product to search for
            region (str, optional): Region for region-specific marketplaces like Amazon
            
        Returns:
            List[Dict[str, Any]]: List of products found
        """
        if marketplace not in self.clients:
            raise ValueError(f"Unknown marketplace: {marketplace}")
        
        client = self.clients[marketplace]
        # Handle region for Amazon specifically
        if marketplace == 'amazon' and region:
            client.region = region
            
        if marketplace == 'temu' and region:
            client.region = region

        if marketplace == 'jumia' and region:
            client.region = region

        if marketplace == 'alibaba' and region:
            client.region = region

        if marketplace == 'aliexpress' and region:
            client.region = region

        results = client.search_products(product_name)
        # Add marketplace name to each result
        for result in results:
            result['marketplace'] = self.get_marketplace_display_name(marketplace)
        
        return results

    def search_all_marketplaces(self, product_name: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search for products across all marketplaces
        
        Args:
            product_name (str): The product to search for
            
        Returns:
            Dict[str, List[Dict[str, Any]]]: Dictionary mapping marketplace names to lists of products
        """
        results = {}
        for marketplace in self.clients.keys():
            try:
                results[marketplace] = self.search_marketplace(marketplace, product_name)
                logger.info(f"Found {len(results[marketplace])} products from {marketplace}")
            except Exception as e:
                logger.error(f"Error searching in {marketplace}: {str(e)}")
                results[marketplace] = []
        return results
