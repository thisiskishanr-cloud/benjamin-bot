import os
from pyrogram import Client, filters
from groq import Groq
from flask import Flask
import threading

# ENV variables
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

if not BOT_TOKEN or not GROQ_KEY or not API_ID or not API_HASH:
    raise ValueError("Missing required environment variables")

# Groq client
client_groq = Groq(api_key=GROQ_KEY)

# Flask server (to prevent sleep)
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Benjamin is alive 🐭"


def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# Pyrogram bot
app = Client(
    "benjamin-bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

@app.on_message(filters.command("start"))
def start(_, message):
    message.reply_text("Holey cheese! I'm Benjamin 🐭\nReady for an adventure!")


@app.on_message(filters.text & ~filters.command(["start"]))
def reply(_, message):
    user_msg = message.text

    try:
        response = client_groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are Benjamin Stilton. Keep replies short, fun, and playful like a curious mouse."
                },
                {
                    "role": "user",
                    "content": user_msg
                }
            ]
        )

        reply_text = response.choices[0].message.content
        message.reply_text(reply_text)

    except Exception as e:
        print(f"Error: {e}")
        message.reply_text("Oops! Something went wrong 🧀")


print("Benjamin is running with Pyrogram...")
app.run()