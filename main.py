import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hii 😊 main *Basanti* hoon 💫\n"
        "Aap se baat karne ke liye yahin hoon 🤍",
        parse_mode="Markdown"
    )

# ===== HELP =====
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start – Bot start karo\n"
        "/help – Commands dekho\n"
        "/broadcast <msg> – Sab users/groups ko message (admin)",
    )

# ===== AI LOGIC =====
def ai_reply_logic(text: str):
    text = text.lower()

    if "tum kon ho" in text or "tum kaun ho" in text:
        return "Main *Basanti* hoon 😊 aapki virtual dost 💛"

    if "kya kar rahi ho" in text:
        return "Abhi aap se baat kar rahi hoon 😊"

    if "kaise ho" in text:
        return "Main bilkul theek hoon 😄 aap kaise ho?"

    if "naam" in text or "name" in text:
        return "Mera naam *Basanti* hai 🌸"

    if "boring" in text:
        return "Arre nahi 😄 thodi baat karo, maza aa jaayega"

    if "good morning" in text:
        return "Good morning ☀️ aaj ka din achha ho"

    if "good night" in text:
        return "Good night 🌙 sweet dreams 😊"

    if "love" in text:
        return "Pyaari si feeling hai ye 😊💫"

    if "thank" in text or "thanks" in text:
        return "Welcome 🤍 mujhe achha laga"

    if "hi" in text or "hello" in text or "hii" in text:
        return "Hii 😊 main yahin hoon"

    return "Achha 😊 thoda aur batao na"

# ===== CHAT =====
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply = ai_reply_logic(update.message.text)
    await update.message.reply_text(reply, parse_mode="Markdown")

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("Basanti bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
