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
        "Namaste 😊\nMain Basanti hoon 🌸\nBaat shuru karo 💬"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()

    if any(x in text for x in ["hi", "hello", "hii"]):
        reply = "Hello 😊 Kya haal hai?"
    elif "kaisi" in text or "kaise" in text:
        reply = "Main bilkul theek hoon 🌸 Tum batao?"
    elif "naam" in text or "name" in text:
        reply = "Mera naam Basanti hai 🤖🌸"
    else:
        reply = "Main sun rahi hoon 😊 Bolo?"

    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, echo))

    print("✅ Basanti STEP 0 running")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
