import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

AMAZON_APIFY_API_TOKEN = os.getenv("AMAZON_APIFY_API_TOKEN")
