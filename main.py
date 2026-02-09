from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ===== CONFIG =====
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

FORBIDDEN_WORDS = [
    "lady", "female", "girl", "telegram bot", "lady ai", "female bot"
]

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hii 😊\n"
        "Main Basanti hoon 🌸\n"
        "Aaram se baat karo — main sun rahi hoon 🤍\n\n"
        "Bas likho, hum baat shuru karte hain 🙂"
    )

# ===== HELP =====
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Main normal baat-cheet ke liye yahin hoon 😊\n"
        "Aap kuch bhi pooch sakte ho — simple, friendly baat."
    )

# ===== SMART CHAT (MY-LIKE STYLE) =====
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    # Safety first
    for word in FORBIDDEN_WORDS:
        if word in text:
            await update.message.reply_text(
                "🙂 Chalo simple baat karte hain.\n"
                "Aap kya discuss karna chahoge?"
            )
            return

    # Identity (safe)
    if "tum kon ho" in text or "tum kaun ho" in text:
        reply = "Main Basanti hoon 😊 aapki baat samajhne ke liye yahin hoon."

    # Feelings / care
    elif "kaise ho" in text:
        reply = "Main theek hoon 😊 aap batao, sab theek?"

    elif "acha nahi lag raha" in text or "sad" in text:
        reply = "Samajh sakti hoon 😌 thoda batao kya hua?"

    # Curiosity
    elif "kya kar" in text:
        reply = "Abhi aap se baat kar rahi hoon 🙂 aur sun rahi hoon."

    # Greetings
    elif "hi" in text or "hello" in text or "hii" in text:
        reply = "Hii 😊 kaise ho?"

    # Thanks
    elif "thank" in text or "thanks" in text:
        reply = "Koi baat nahi 🤍 mujhe achha laga."

    # Default (very important – natural)
    else:
        reply = "Samajh gayi 🙂 thoda aur batao."

    await update.message.reply_text(reply)

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("Basanti (friendly assistant-style) running...")
    app.run_polling()

if __name__ == "__main__":
    main()
