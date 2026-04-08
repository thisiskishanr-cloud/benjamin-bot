from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import random

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey! I'm Benjamin 🐭\nSay hi to me!")

# reply to "hi"
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def reply(update, context):
    user_msg = update.message.text

    try:
        prompt = f"""
        You are Benjamin from Geronimo Stilton.
        You are smart, curious, friendly, playful.
        Keep replies short and fun.

        User: {user_msg}
        """

        response = client.responses.create(
            model="gpt-4o-mini",
            input=prompt
        )

        await update.message.reply_text(response.output_text)

    except Exception as e:
        await update.message.reply_text("Oops! Something went wrong 🧀")
        print(e)

# main app
app = ApplicationBuilder().token("7964085894:AAHfX67Yla8H7i7P1mVjoDszQp1IglVF5P0").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("Bot is running...")
app.run_polling()