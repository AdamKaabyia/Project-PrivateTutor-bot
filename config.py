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
import requests

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# States for conversation handlers
REGISTER_NAME, REGISTER_EMAIL, REGISTER_USERNAME, REGISTER_PASSWORD = range(4)
LOGIN_EMAIL, LOGIN_PASSWORD = range(2)
