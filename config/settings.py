import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
