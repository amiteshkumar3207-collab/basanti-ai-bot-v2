from telegram.ext import ApplicationBuilder, CommandHandler
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update, context):
    await update.message.reply_text(
        "🌼 Namaste! Main Basanti hoon.\nMain theek se chal rahi hoon 🙂"
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.run_polling()
