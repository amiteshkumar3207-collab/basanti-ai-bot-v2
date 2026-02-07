import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Namaste 😊\nMain Basanti hoon 🌸\nBot bilkul theek chal raha hai ✅"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "hello" in text or "hi" in text:
        reply = "Hello 😊 Kya haal hai?"
    elif "kaisi ho" in text or "kaise ho" in text:
        reply = "Main bilkul theek hoon 🌸 Tum batao?"
    elif "name" in text:
        reply = "Mera naam Basanti hai 🤖🌸"
    else:
        reply = "Main sun rahi hoon 😊 Bolo?"

    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("🤖 Basanti STEP 0 running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
