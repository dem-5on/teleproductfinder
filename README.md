# SmartShopperBot - Multi-Marketplace Deal Finder

## Project Overview

The **SmartShopperBot** is a Telegram bot that helps you find the best deals across multiple online marketplaces. Currently supported platforms include:
- Amazon (via Apify scraping)
- Temu
- Jumia
- Alibaba

The bot takes your product description or name and searches across these platforms to find the best deals. It compares listings based on various factors including:
- Price
- Reviews and ratings
- Delivery time and cost
- Seller reputation
- Platform reliability

## Features

- 🌍 **Multi-Marketplace Support**: Search across multiple e-commerce platforms simultaneously
- 💬 **Conversational Interface**: Natural language processing for better search understanding
- 🔍 **Smart Filtering**: Advanced algorithms to find genuine deals and filter out unreliable listings
- 📊 **Comparative Analysis**: Side-by-side comparison of deals across different platforms
- 🚀 **Docker Support**: Easy deployment using Docker containers

## How to Run the Bot

### Using Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/dem-5on/teleproductfinder.git
   cd teleproductfinder
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

### Manual Installation

1. **Clone and setup:**
   ```bash
   git clone https://github.com/dem-5on/teleproductfinder.git
   cd teleproductfinder
   python -m venv env
   source env/bin/activate  # On Windows: .\env\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Run the bot:**
   ```bash
   python main.py
   ```

## Environment Variables

The following environment variables need to be set in your .env file:

```bash
# Required
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
APIFY_API_TOKEN=your_apify_token_here

# Optional (for Amazon Product API)
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_ASSOCIATE_TAG=your_amazon_associate_tag_here
AWS_REGION=your_aws_region_here
```

## Project Structure

```
├── Dockerfile              # Container configuration
├── docker-compose.yml     # Docker service orchestration
├── requirements.txt       # Python dependencies
├── main.py               # Application entry point
├── telegram_bot/
│   ├── handler.py        # Telegram bot command handlers
│   └── message_formatter.py  # Response formatting
├── marketplaces/
│   ├── amazon/           # Amazon integration via Apify
│   ├── temu/            # Temu marketplace integration
│   ├── jumia/           # Jumia marketplace integration
│   └── alibaba/         # Alibaba marketplace integration
├── utils/
│   ├── scoring.py       # Deal scoring algorithms
│   └── marketplace_manager.py  # Marketplace coordination
└── config/
    └── settings.py      # Configuration management
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m "feat: add amazing feature"`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
