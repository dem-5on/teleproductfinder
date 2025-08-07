# SmartShopperBot - Online Shops Best Deal Finder

## Project Overview

The **SmartShopperBot** is a Telegram bot that helps you find the best deals for products on **Amazon, temu, alibaba, jumia**. The bot takes in the product description or name and, optionally, the region (eg. Amazon country domain). It then compares listings from multiple sellers and returns the **best deal** based on **price**, **reviews**, **ratings**, **delivery time**, and more. If no region is provided, the bot defaults to **amazon.com** (USA).

## How to Run the Bot

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/smartshopper-bot.git
    cd smartshopper-bot
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your environment variables:**

    Create a `.env` file in the `smartshopper_bot` directory and add your credentials:
    ```
    TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
    AMAZON_ACCESS_KEY=YOUR_AMAZON_ACCESS_KEY
    AMAZON_SECRET_KEY=YOUR_AMAZON_SECRET_KEY
    AMAZON_ASSOCIATE_TAG=YOUR_AMAZON_ASSOCIATE_TAG
    ```

4.  **Run the bot:**
    ```bash
    python main.py
    ```

## Folder Structure

```
smartshopper_bot/
├── main.py                    # Main file handling bot commands and logic
├── telegram_bot/
│   ├── handler.py             # Handles interactions with users
│   └── message_formatter.py   # Formats messages and responses
├── amazon_api/
│   ├── client.py              # Amazon API calls (region-specific handling)
│   └── product_selector.py    # Logic to filter and compare product listings
├── utils/
│   └── scoring.py             # Scoring algorithm for best deal selection
└── config/
    └── settings.py           # Store Amazon API credentials and settings
```
