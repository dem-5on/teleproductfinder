import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, ConversationHandler, CommandHandler, 
    CallbackQueryHandler, MessageHandler, filters
)
from marketplace_api import MarketplaceManager
from .message_formatter import format_product_message

# Configure logging
logger = logging.getLogger(__name__)

# Conversation states
CHOOSING_MARKETPLACE = 1
ENTERING_SEARCH = 2

class BestDealHandler:
    def __init__(self):
        self.marketplace_manager = MarketplaceManager()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler for the /start command"""
        user = update.effective_user
        logger.info(f"New user started the bot: {user.id} ({user.username})")
        welcome_message = (
            f"👋 Hi {user.first_name}!\n\n"
            "I can help you find the best deals across different marketplaces. Here's how to use me:\n\n"
            "1. Use /find to start a product search\n"
            "2. Choose a specific marketplace or search all at once\n"
            "3. Enter your search term\n\n"
            "Try it now with /find! 🛍️"
        )
        await update.message.reply_text(welcome_message)

    async def find_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handles the /find command"""
        keyboard = [
            [
                InlineKeyboardButton("Search All", callback_data="search_all"),
                InlineKeyboardButton("Choose Marketplace", callback_data="search_single")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "How would you like to search?",
            reply_markup=reply_markup
        )
        return CHOOSING_MARKETPLACE

    async def marketplace_choice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle marketplace selection"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "search_all":
            await query.edit_message_text("Enter your search term to find products across all marketplaces:")
            context.user_data['search_type'] = 'all'
            return ENTERING_SEARCH
        
        # Show marketplace options
        keyboard = [
            [InlineKeyboardButton(
                self.marketplace_manager.get_marketplace_display_name(market),
                callback_data=f"market_{market}"
            )] for market in self.marketplace_manager.get_available_marketplaces()
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "Choose a marketplace to search from:",
            reply_markup=reply_markup
        )
        return CHOOSING_MARKETPLACE

    async def handle_marketplace_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle specific marketplace selection"""
        query = update.callback_query
        await query.answer()
        
        marketplace = query.data.replace("market_", "")
        context.user_data['marketplace'] = marketplace
        context.user_data['search_type'] = 'single'
        
        await query.edit_message_text(
            f"Enter your search term to find products on {self.marketplace_manager.get_marketplace_display_name(marketplace)}:"
        )
        return ENTERING_SEARCH

    async def handle_search(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process the search term and return results"""
        search_term = update.message.text
        search_type = context.user_data.get('search_type')
        
        status_message = await update.message.reply_text("🔍 Searching for products...")
        
        try:
            if search_type == 'all':
                results = self.marketplace_manager.search_all_marketplaces(search_term)
                # Combine all results and find best deals
                all_products = []
                for marketplace_results in results.values():
                    all_products.extend(marketplace_results)
                
                if not all_products:
                    await status_message.edit_text(
                        "No products found in any marketplace. Try different search terms."
                    )
                    return ConversationHandler.END
                
                # Format and send results
                messages = ["🌟 Best deals across marketplaces:\n"]
                for marketplace, products in results.items():
                    if products:
                        best_product = max(products, key=lambda x: float(x.get('rating', 0) or 0))
                        messages.append(f"\n🏪 {self.marketplace_manager.get_marketplace_display_name(marketplace)}:")
                        messages.append(format_product_message(best_product))
                
                await status_message.edit_text(
                    "\n".join(messages),
                    parse_mode="Markdown"
                )
                
            else:
                marketplace = context.user_data.get('marketplace')
                products = self.marketplace_manager.search_marketplace(marketplace, search_term)
                
                if not products:
                    await status_message.edit_text(
                        f"No products found on {self.marketplace_manager.get_marketplace_display_name(marketplace)}. "
                        "Try different search terms."
                    )
                    return ConversationHandler.END
                
                # Get best product based on rating
                best_product = max(products, key=lambda x: float(x.get('rating', 0) or 0))
                await status_message.edit_text(
                    format_product_message(best_product),
                    parse_mode="Markdown"
                )
                
        except Exception as e:
            logger.error(f"Error during search: {str(e)}")
            await status_message.edit_text(
                "😔 Sorry, something went wrong during the search. Please try again later."
            )
            
        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancels and ends the conversation"""
        await update.message.reply_text(
            "Search cancelled. Use /find to start a new search!"
        )
        return ConversationHandler.END

    def get_conversation_handler(self):
        """Returns the conversation handler for the bot"""
        return ConversationHandler(
            entry_points=[CommandHandler('find', self.find_command)],
            states={
                CHOOSING_MARKETPLACE: [
                    CallbackQueryHandler(self.marketplace_choice, pattern="^search_"),
                    CallbackQueryHandler(self.handle_marketplace_selection, pattern="^market_")
                ],
                ENTERING_SEARCH: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_search)
                ]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )