from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ================= CONFIG =================

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

FORBIDDEN_WORDS = [
    "lady",
    "female",
    "girl",
    "ai",
    "telegram bot",
    "lady ai",
    "female bot"
]

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hii 😊\n"
        "Main Basanti hoon 🌸\n"
        "Aap se baat karne ke liye yahin hoon.\n\n"
        "Kuch bhi normal baat karni ho to batao 🙂"
    )

# ================= CHAT =================

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    # Forbidden words filter
    for word in FORBIDDEN_WORDS:
        if word in text:
            await update.message.reply_text(
                "😊 bas simple baat karte hain na.\n"
                "Aap kya baat karna chahoge?"
            )
            return

    # Smart replies
    if "kaise ho" in text:
        reply = "Main theek hoon 😊 aap batao?"
    elif "kya kar" in text:
        reply = "Bas aap se baat kar rahi hoon 🙂"
    elif "tum kon ho" in text or "kaun ho" in text:
        reply = "Main Basanti hoon 🌸"
    elif "hii" in text or "hello" in text:
        reply = "Hii 😊 kaise ho?"
    else:
        reply = "😊 haan sun rahi hoon.\nAur batao?"

    await update.message.reply_text(reply)

# ================= MAIN =================

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("Basanti bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
