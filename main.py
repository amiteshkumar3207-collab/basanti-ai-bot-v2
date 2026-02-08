from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os
from ai_engine import ask_ai

TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    print("TELEGRAM_TOKEN missing")
    exit(1)

async def start(update, context):
    await update.message.reply_text("Basanti AI Bot alive 🤖")

async def chat(update, context):
    reply = ask_ai(update.message.text)
    await update.message.reply_text(reply)

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
