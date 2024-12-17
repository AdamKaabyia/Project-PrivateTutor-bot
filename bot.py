import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ApplicationBuilder,
    ConversationHandler,
    filters,
    CallbackContext,
)
from register import *
from login import *

# load_dotenv()
#
# API_BASE_URL = os.getenv("API_BASE_URL")
# BOT_TOKEN = os.getenv("BOT_TOKEN")
#
# # States for conversation handlers
# REGISTER_NAME, REGISTER_EMAIL, REGISTER_USERNAME, REGISTER_PASSWORD = range(4)
# LOGIN_EMAIL, LOGIN_PASSWORD = range(2)

# User state management
user_sessions = {}

# Handlers for the start and help commands
async def start(update: Update, context: CallbackContext) -> None:
    """Start command to greet the user."""
    await update.message.reply_text(
        "Welcome to the Student-Teacher Scheduler Bot!\n"
        "Use /help to see all available commands."
    )


async def help_command(update: Update, context: CallbackContext) -> None:
    """Help command to display all supported commands."""
    help_text = (
        "Here are the available commands:\n"
        "/start - Start the bot and see a welcome message.\n"
        "/help - Show this help message.\n"
        "/register - Register a new account.\n"
        "/login - Log in to your account.\n"
    )
    await update.message.reply_text(help_text)


# Main function
def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Conversation handlers for registration and login
    register_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("register", register_start)],
        states={
            REGISTER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_name)],
            REGISTER_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_email)],
            REGISTER_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_username)],
            REGISTER_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_password)],
        },
        fallbacks=[CommandHandler("cancel", register_cancel)],
    )

    login_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("login", login_start)],
        states={
            LOGIN_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, login_email)],
            LOGIN_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, login_password)],
        },
        fallbacks=[CommandHandler("cancel", login_cancel)],
    )

    # Add handlers to the application
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(register_conv_handler)
    application.add_handler(login_conv_handler)

    # Run the bot
    application.run_polling()


if __name__ == "__main__":
    main()
