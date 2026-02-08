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

# WhatsApp-style replies (NO AI, NO memory)
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()

    if text in ["hi", "hii", "hello"]:
        reply_text = "Hii 😊"
    elif "kaisi" in text or "kaise" in text:
        reply_text = "Theek hoon 🌸 tum?"
    elif "naam" in text or "name" in text:
        reply_text = "Basanti 😄"
    elif "thanks" in text or "thank" in text:
        reply_text = "Arre koi baat nahi 😊"
    else:
        reply_text = "Haan, bolo 🙂"

    await update.message.reply_text(reply_text)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, reply))

    print("✅ Basanti STEP 1 running (WhatsApp style)")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
