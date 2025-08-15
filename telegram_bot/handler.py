import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, ConversationHandler, CommandHandler, 
    CallbackQueryHandler, MessageHandler, filters, Application
)
from marketplace_api import MarketplaceManager
from .message_formatter import format_product_message

# Configure logging
logger = logging.getLogger(__name__)

# Conversation states
MAIN_MENU = 0
CHOOSING_MARKETPLACE = 1
ENTERING_SEARCH = 2

class BestDealHandler:
    def __init__(self):
        self.marketplace_manager = MarketplaceManager()

    def get_start_keyboard(self):
        """Returns the initial start keyboard"""
        keyboard = [[InlineKeyboardButton("🚀 Start Bot", callback_data="start_bot")]]
        return InlineKeyboardMarkup(keyboard)

    def get_main_menu_keyboard(self):
        """Returns the main menu keyboard with Find button"""
        keyboard = [[InlineKeyboardButton("🔍 Find Products", callback_data="find_products")]]
        return InlineKeyboardMarkup(keyboard)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler for the /start command - shows start button"""
        user = update.effective_user
        logger.info(f"New user started the bot: {user.id} ({user.username})")
        
        welcome_message = (
            f"👋 Welcome to Product Finder Bot!\n\n"
            "Click the button below to get started and find amazing deals across different marketplaces! 🛍️"
        )
        
        await update.message.reply_text(
            welcome_message,
            reply_markup=self.get_start_keyboard()
        )
        return MAIN_MENU

    async def handle_start_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the start button click"""
        query = update.callback_query
        logger.info(f"Start button clicked by user: {query.from_user.id}")
        
        try:
            await query.answer()
            
            user = update.effective_user
            welcome_message = (
                f"👋 Hi {user.first_name}!\n\n"
                "I can help you find the best deals across different marketplaces. Here's how it works:\n\n"
                "1. Click 'Find Products' to start searching\n"
                "2. Choose to search all marketplaces or pick a specific one\n"
                "3. Enter your search term\n"
                "4. Get the best deals!\n\n"
                "Ready to find some great deals? 🎯"
            )
            
            await query.edit_message_text(
                welcome_message,
                reply_markup=self.get_main_menu_keyboard()
            )
            logger.info(f"Successfully edited message for user: {query.from_user.id}")
            
        except Exception as e:
            logger.error(f"Error handling start button: {str(e)}")
            # Fallback: send a new message instead of editing
            await query.message.reply_text(
                f"👋 Hi {user.first_name}!\n\n"
                "I can help you find the best deals across different marketplaces. Here's how it works:\n\n"
                "1. Click 'Find Products' to start searching\n"
                "2. Choose to search all marketplaces or pick a specific one\n"
                "3. Enter your search term\n"
                "4. Get the best deals!\n\n"
                "Ready to find some great deals? 🎯",
                reply_markup=self.get_main_menu_keyboard()
            )
        
        return MAIN_MENU

    async def handle_find_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the find products button click"""
        query = update.callback_query
        logger.info(f"Find button clicked by user: {query.from_user.id}")
        await query.answer()
        
        keyboard = [
            [
                InlineKeyboardButton("🌐 Search All", callback_data="search_all"),
                InlineKeyboardButton("🏪 Choose Marketplace", callback_data="search_single")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "How would you like to search for products?",
            reply_markup=reply_markup
        )
        return CHOOSING_MARKETPLACE

    async def find_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handles the /find command (fallback for users who type commands)"""
        keyboard = [
            [
                InlineKeyboardButton("🌐 Search All", callback_data="search_all"),
                InlineKeyboardButton("🏪 Choose Marketplace", callback_data="search_single")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "How would you like to search for products?",
            reply_markup=reply_markup
        )
        return CHOOSING_MARKETPLACE

    async def marketplace_choice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle marketplace selection"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "search_all":
            keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_search_options")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "Enter your search term to find products across all marketplaces:",
                reply_markup=reply_markup
            )
            context.user_data['search_type'] = 'all'
            return ENTERING_SEARCH
        
        # Show marketplace options
        keyboard = [
            [InlineKeyboardButton(
                self.marketplace_manager.get_marketplace_display_name(market),
                callback_data=f"market_{market}"
            )] for market in self.marketplace_manager.get_available_marketplaces()
        ]
        
        # Add back button
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back_to_search_options")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "Choose a marketplace to search from:",
            reply_markup=reply_markup
        )
        return CHOOSING_MARKETPLACE

    async def handle_back_to_search_options(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle back button to return to search options"""
        query = update.callback_query
        await query.answer()
        
        keyboard = [
            [
                InlineKeyboardButton("🌐 Search All", callback_data="search_all"),
                InlineKeyboardButton("🏪 Marketplace", callback_data="search_single")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "How would you like to search for products?",
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
                    await status_message.edit_text("❌ No products found in any marketplace. Try different search terms.")
                    # Return to main menu after failed search
                    await self.return_to_main_menu(update, context)
                    return MAIN_MENU
                
                # Format and send results
                await status_message.edit_text("✅ Found great deals! Here are the best products:")
                
                for marketplace, products in results.items():
                    if products:
                        best_product = max(products, key=lambda x: float(x.get('rating', 0) or 0))
                        message, url = format_product_message(best_product)
                        
                        reply_markup = None
                        if url:
                            keyboard = [[InlineKeyboardButton("🛒 View Product", url=url)]]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                        
                        marketplace_name = self.marketplace_manager.get_marketplace_display_name(marketplace)
                        full_message = f"🏪 **{marketplace_name}**\n{message}"
                        
                        await update.message.reply_text(
                            text=full_message,
                            reply_markup=reply_markup,
                            parse_mode="Markdown"
                        )
                
            else:
                marketplace = context.user_data.get('marketplace')
                products = self.marketplace_manager.search_marketplace(marketplace, search_term)
                
                if not products:
                    marketplace_name = self.marketplace_manager.get_marketplace_display_name(marketplace)
                    await status_message.edit_text(
                        f"❌ No products found on {marketplace_name}. Try different search terms."
                    )
                    # Return to main menu after failed search
                    await self.return_to_main_menu(update, context)
                    return MAIN_MENU
                
                # Get best product based on rating
                best_product = max(products, key=lambda x: float(x.get('rating', 0) or 0))
                message, url = format_product_message(best_product)
                
                reply_markup = None
                if url:
                    keyboard = [[InlineKeyboardButton("🛒 View Product", url=url)]]
                    reply_markup = InlineKeyboardMarkup(keyboard)

                
        except Exception as e:
            logger.error(f"Error during search: {str(e)}")
            await status_message.edit_text(
                "😔 Sorry, something went wrong during the search. Please try again."
            )
        
        # Return to main menu after successful search
        await self.return_to_main_menu(update, context)
        return MAIN_MENU

    async def return_to_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Return to main menu with Find button"""
        await update.message.reply_text(
            "🎉 Search complete! Ready for another search?",
            reply_markup=self.get_main_menu_keyboard()
        )

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancels and ends the conversation"""
        await update.message.reply_text(
            "❌ Search cancelled.",
            reply_markup=self.get_main_menu_keyboard()
        )
        return MAIN_MENU

    def get_conversation_handler(self):
        """Returns the conversation handler for the bot"""
        return ConversationHandler(
            entry_points=[
                CommandHandler('start', self.start),
                CommandHandler('find', self.find_command),
                # Add callback handler as entry point for when conversation is None
                CallbackQueryHandler(self.handle_start_button, pattern="^start_bot$")
            ],
            states={
                MAIN_MENU: [
                    CallbackQueryHandler(self.handle_start_button, pattern="^start_bot$"),
                    CallbackQueryHandler(self.handle_find_button, pattern="^find_products$")
                ],
                CHOOSING_MARKETPLACE: [
                    CallbackQueryHandler(self.marketplace_choice, pattern="^search_"),
                    CallbackQueryHandler(self.handle_marketplace_selection, pattern="^market_"),
                    CallbackQueryHandler(self.handle_back_to_search_options, pattern="^back_to_search_options$")
                ],
                ENTERING_SEARCH: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_search),
                    CallbackQueryHandler(self.handle_back_to_search_options, pattern="^back_to_search_options$")
                ]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)],
            allow_reentry=True
        )