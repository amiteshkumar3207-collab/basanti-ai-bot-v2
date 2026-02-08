import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from memory import set_name, get_name

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hii 😊\nMain Basanti hoon 🌸\nTumhara naam kya hai?"
    )

# Chat with memory
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()
    user_id = update.effective_user.id

    if text in ["hi", "hii", "hello"]:
        reply_text = "Hii 😊"
    elif "mera naam" in text:
        # example: "mera naam deepak"
        name = text.replace("mera naam", "").strip().title()
        if name:
            set_name(user_id, name)
            reply_text = f"Achha {name} 😊 Yaad rakhungi."
        else:
            reply_text = "Naam theek se batao 🙂"
    elif "kaisi" in text or "kaise" in text:
        name = get_name(user_id)
        if name:
            reply_text = f"Theek hoon 🌸 {name}, tum?"
        else:
            reply_text = "Theek hoon 🌸 tum?"
    elif "naam" in text or "name" in text:
        reply_text = "Basanti 😄"
    else:
        name = get_name(user_id)
        if name:
            reply_text = f"Haan {name}, bolo 🙂"
        else:
            reply_text = "Haan, bolo 🙂"

    await update.message.reply_text(reply_text)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, reply))

    print("✅ Basanti STEP 2 running (memory)")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
