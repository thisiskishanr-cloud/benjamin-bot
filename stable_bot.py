
import sys
import types

imghdr = types.ModuleType("imghdr")
imghdr.what = lambda *args: None
sys.modules["imghdr"] = imghdr

import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from groq import Groq
from flask import Flask
import threading

# 1. SETUP - Use environment variables for security!
# In your terminal, run: export TELEGRAM_TOKEN='your_token' and export GROQ_API_KEY='your_key'
TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")
if not TOKEN or not GROQ_KEY:
    raise ValueError("Missing TELEGRAM_TOKEN or GROQ_API_KEY environment variables")


client = Groq(api_key=GROQ_KEY)

# Tiny Flask server for uptime checks
app_flask = Flask('')

@app_flask.route('/')
def home():
    return "Benjamin is alive 🐭"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

# Run Flask in background thread
threading.Thread(target=run_flask, daemon=True).start()


# /start command
def start(update, context):
    update.message.reply_text("Holey cheese! I'm Benjamin 🐭\nReady for an adventure? Say hi!")

# AI Reply Logic
def reply(update, context):
    user_msg = update.message.text

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are Benjamin Stilton from Geronimo Stilton. You are young, smart, playful, and adventurous. Keep replies short and fun with mouse-related expressions."
                },
                {
                    "role": "user",
                    "content": user_msg
                }
            ]
        )
        reply_text = response.choices[0].message.content
        update.message.reply_text(reply_text)

    except Exception as e:
        print(f"Error: {e}")
        update.message.reply_text("Oops! My whiskers are tingling... something went wrong! 🧀")

# Main Application
if __name__ == "__main__":
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))

    print("Benjamin is awake and looking for cheese... (Bot is running)")
    updater.start_polling()
    updater.idle()