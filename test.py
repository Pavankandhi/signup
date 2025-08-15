import os
import re
import pickle
import subprocess
import time
from datetime import datetime
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

DATA_FILE = "users.pkl"
ADMIN_ID = int(os.getenv("ADMIN_ID", "7539992077"))  # Get from environment
TOKEN = os.getenv("TELEGRAM_TOKEN")  # Get from environment

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "rb") as f:
        users = pickle.load(f)
else:
    users = {}

def save_data():
    with open(DATA_FILE, "wb") as f:
        pickle.dump(users, f)

# [Rest of the code remains the same as your original file]
# ... (all your existing functions)

if __name__ == "__main__":
    if not TOKEN:
        print("Error: TELEGRAM_TOKEN environment variable is not set!")
        sys.exit(1)
        
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(CommandHandler("disapprove", disapprove))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()