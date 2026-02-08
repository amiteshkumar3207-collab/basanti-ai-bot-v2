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

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hii 😊\nMain Basanti hoon 🌸\nBaat shuru karo 💬"
    )

# WhatsApp-style chat
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()

    if any(x in text for x in ["hi", "hello", "hii"]):
        reply = "Hii 😊"
    elif "kaisi" in text or "kaise" in text:
        reply = "Theek hoon 🌸 tum batao?"
    elif "naam" in text or "name" in text:
        reply = "Basanti 😄"
    elif "thanks" in text or "thank" in text:
        reply = "Arre koi baat nahi 😊"
    else:
        reply = "Haan sun rahi hoon 👂 bolo"

    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, chat))

    print("✅ Basanti STEP 1 running (WhatsApp style)")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
