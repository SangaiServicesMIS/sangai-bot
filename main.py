
import os
import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Load services from JSON file
def load_services():
    with open("services.json", "r") as f:
        return json.load(f)

# Define buttons
def main_menu_buttons():
    return [[
        InlineKeyboardButton("Learn About Services", callback_data="learn_services"),
        InlineKeyboardButton("Book Services", callback_data="book_services")
    ], [
        InlineKeyboardButton("Get Customer Care Contact Number", callback_data="get_contact")
    ]]

def back_to_main_button():
    return [[InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")]]

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Sangai Support Chat. Please choose an option:",
        reply_markup=InlineKeyboardMarkup(main_menu_buttons())
    )

# Callback handler
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "main_menu":
        await query.edit_message_text(
            "Main Menu:",
            reply_markup=InlineKeyboardMarkup(main_menu_buttons())
        )

    elif query.data == "learn_services":
        services = load_services()
        message = "Available Services:\n"
        for service in services:
            message += f"\n{service['name']}: {service['description']}"
        await query.edit_message_text(
            message,
            reply_markup=InlineKeyboardMarkup(back_to_main_button())
        )

    elif query.data == "book_services":
        await query.edit_message_text(
            "You can book our services using the link below:\nhttps://forms.gle/TYDKUu4JYxywHtPq5",
            reply_markup=InlineKeyboardMarkup(back_to_main_button())
        )

    elif query.data == "get_contact":
        await query.edit_message_text(
            "Customer Care Contact:\n+91-6009384285",
            reply_markup=InlineKeyboardMarkup(back_to_main_button())
        )

# Setup logging
logging.basicConfig(level=logging.INFO)

# Main function to run the bot
async def main():
    token = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
