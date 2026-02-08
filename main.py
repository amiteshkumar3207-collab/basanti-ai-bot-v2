
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os
from ai_engine import ask_ai   # ← THIS MUST WORK NOW

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update, context):
    await update.message.reply_text("Basanti AI Bot online 🤖")

async def chat(update, context):
    text = update.message.text
    await update.message.chat.send_action("typing")
    try:
        reply = ask_ai(text)
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("Error aaya, baad me try karo.")

app = Application.builder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
