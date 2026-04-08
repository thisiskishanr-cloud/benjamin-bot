import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

# 1. SETUP - Use environment variables for security!
# In your terminal, run: export TELEGRAM_TOKEN='your_token' and export GROQ_API_KEY='your_key'
TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")
if not TOKEN or not GROQ_KEY:
    raise ValueError("Missing TELEGRAM_TOKEN or GROQ_API_KEY environment variables")

client = Groq(api_key=GROQ_KEY)


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Holey cheese! I'm Benjamin 🐭\nReady for an adventure? Say hi!")

# AI Reply Logic
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        await update.message.reply_text(reply_text)

    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("Oops! My whiskers are tingling... something went wrong! 🧀")

# Main Application
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    print("Benjamin is awake and looking for cheese... (Bot is running)")
    app.run_polling()