import logging
from telegram.ext import Application, CommandHandler

from config import settings
from telegram_bot.handler import BestDealHandler

# Configure logging with more detailed format
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    level=logging.DEBUG  # Changed to DEBUG level for more detailed logs
)
logger = logging.getLogger(__name__)

# Ensure all loggers are set to DEBUG
logging.getLogger('telegram').setLevel(logging.DEBUG)
logging.getLogger('telegram.ext').setLevel(logging.DEBUG)
logging.getLogger('httpx').setLevel(logging.INFO)  # Reduce noise from HTTP requests
logging.getLogger('httpcore').setLevel(logging.INFO)

def main():
    """
    Main function to run the bot.
    """
    logger.info("Starting the bot...")
    try:
        logger.info(f"Using bot token: {settings.TELEGRAM_BOT_TOKEN[:5]}...")
        application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
        logger.info("Bot application built successfully")
        
        # Create handler instance
        handler = BestDealHandler()
        
        # Register command handlers
        application.add_handler(CommandHandler("start", handler.start))
        application.add_handler(handler.get_conversation_handler())
        logger.info("Command handlers registered")

        # Start the bot until you press Ctrl-C
        logger.info("Starting polling...")
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Error starting bot: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (Ctrl-C)")
    except Exception as e:
        logger.error(f"Bot stopped due to error: {str(e)}", exc_info=True)
