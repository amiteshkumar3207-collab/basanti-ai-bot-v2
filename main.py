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
from ai_engine import ask_ai

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hii 😊 Main Basanti hoon 🌸\nTumhara naam kya hai?"
    )

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()
    user_id = update.effective_user.id

    # Simple rules first
    if text in ["hi", "hii", "hello"]:
        reply_text = "Hii 😊"

    elif "mera naam" in text:
        name = text.replace("mera naam", "").strip().title()
        if name:
            set_name(user_id, name)
            reply_text = f"Achha {name} 😊 Yaad rakhungi."
        else:
            reply_text = "Naam theek se batao 🙂"

    elif "kaisi" in text or "kaise" in text:
        name = get_name(user_id)
        reply_text = f"Theek hoon 🌸 {name}, tum?" if name else "Theek hoon 🌸 tum?"

    elif "naam" in text or "name" in text:
        reply_text = "Basanti 😄"

    else:
        # AI fallback
        reply_text = ask_ai(update.message.text)

    await update.message.reply_text(reply_text)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, reply))
    print("✅ Basanti STEP 3 running (AI enabled)")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
