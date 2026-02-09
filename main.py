import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ===== START COMMAND =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hii 😊 main *Basanti* hoon 💕\n"
        "Aap se baat karne ke liye yahin hoon 🥰",
        parse_mode="Markdown"
    )

# ===== AI REPLY LOGIC =====
def ai_reply_logic(text: str):
    text = text.lower()

    if "tum kon ho" in text or "tum kaun ho" in text:
        return "Main *Basanti* hoon 😊 ek lady AI Telegram bot 👩‍💻"

    if "kya kar rahi ho" in text:
        return "Bas aap se baat kar rahi hoon 💕"

    if "kaise ho" in text:
        return "Main bilkul theek hoon 😊 aap kaise ho?"

    if "naam" in text or "name" in text:
        return "Mera naam *Basanti* hai 😄"

    if "help" in text:
        return (
            "/start – Bot start karo\n"
            "/help – Commands dekho\n"
            "/broadcast <msg> – Sabko message (admin)"
        )

    if "thank" in text or "thanks" in text:
        return "Aww 😊 welcome 💖"

    if "hi" in text or "hello" in text or "hii" in text:
        return "Hii 😊 main yahin hoon"

    return "Achha 😊 thoda aur batao na 💬"

# ===== MESSAGE HANDLER =====
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply = ai_reply_logic(update.message.text)
    await update.message.reply_text(reply, parse_mode="Markdown")

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 Basanti bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
