from apify_client import ApifyClient
import logging
import httpx

from config import settings

logger = logging.getLogger(__name__)

class AmazonClient:
    def __init__(self, region="com"):
        self.region = region
        self.client = ApifyClient(settings.AMAZON_APIFY_API_TOKEN)

    def _process_review_data(self, item):
        """
        Process review-related data from an item.
        This method can be extended later to include AI-powered review analysis.
        
        Args:
            item (dict): Raw item data from Apify
            
        Returns:
            dict: Processed review data including rating, count, and any future analysis
        """
        review_data = {
            'rating': float(item.get('rating') or item.get('stars', 0) or 0),
            'reviews_count': int(item.get('reviewsCount') or item.get('numberOfReviews', 0) or 0),
            'review_analysis': None  # Placeholder for future AI analysis
        }
        
        # Future enhancement: Add AI-powered review analysis here
        # review_data['review_analysis'] = self._analyze_reviews(item.get('reviews', []))
        
        return review_data

    def search_products(self, product_name):
        """
        Searches for products on Amazon using the Apify Amazon crawler
        """
        try:
            search_url = f"https://www.amazon.{self.region}/s?k={product_name.replace(' ', '+')}"
            logger.info(f"Searching Amazon with URL: {search_url}")
            
            run_input = {
                "categoryOrProductUrls": [{"url": search_url}],
                "maxItemsPerStartUrl": 20,  # Limit to 20 items for faster response
                "proxyCountry": "AUTO_SELECT_PROXY_COUNTRY",
                "maxOffers": 0,
                "scrapeSellers": False,
                # Disable enhanced content scraping to avoid non-critical warnings
                "ensureLoadedProductDescriptionFields": False,
                "useCaptchaSolver": False,
                "scrapeProductVariantPrices": False,
                "scrapeProductDetails": False,  # Changed to false to avoid A+ content errors
                "locationDeliverableRoutes": [
                    "SEARCH",  # Only search results needed
                ],
            }

            # Run the Actor and wait for it to finish
            logger.debug("Starting Apify actor run...")
            run = self.client.actor("junglee/Amazon-crawler").call(run_input=run_input)
            
            products = []
            logger.debug("Processing search results...")
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                try:
                    # Extract data with more lenient checks
                    title = item.get('title', '')
                    if not title:
                        logger.debug("Skipping product with no title")
                        continue

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

                    # Process review data separately
                    review_data = self._process_review_data(item)
                    
                    # Create product with all possible fields
                    product = {
                        'title': title,
                        'price': price,
                        'url': url,
                        'is_prime': item.get('isAmazonPrime') or item.get('isPrime', False),
                        'asin': item.get('asin', ''),
                        **review_data  # Include processed review data
                    }

                    # Only skip if we really don't have essential data
                    if not title or not url:
                        logger.debug(f"Skipping product missing essential data: {title}")
                        continue
                        
                    products.append(product)
                except Exception as e:
                    logger.debug(f"Error processing product data: {str(e)}")
                    continue

            logger.info(f"Found {len(products)} products from Apify")
            return products

        except Exception as e:
            logger.error(f"Error in Apify search: {str(e)}")
            raise

        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {str(e)}")
            raise Exception(f"Failed to fetch products from Amazon: {str(e)}")
        except Exception as e:
            logger.error(f"Error searching products: {str(e)}")
            raise Exception(f"An error occurred while searching products: {str(e)}")