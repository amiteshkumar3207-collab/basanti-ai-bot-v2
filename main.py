import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)

# ---------- LOGGING ----------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ---------- ENV ----------
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not BOT_TOKEN or not GEMINI_API_KEY:
    raise ValueError("BOT_TOKEN or GEMINI_API_KEY missing")

# ---------- GEMINI ----------
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = """
You are Basanti.
You are friendly, warm, smart and natural.
You do NOT say you are an AI, bot, or lady bot.
You talk like a real human friend.
You reply differently every time.
You never repeat the same sentence again and again.
Use simple Hindi/English mix.
"""

# ---------- HANDLERS ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hii 😊 main yahin hoon.\nAaram se baat karo 💛"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        prompt = f"{SYSTEM_PROMPT}\nUser: {user_text}\nBasanti:"
        response = model.generate_content(prompt)
        reply = response.text.strip()

        if not reply:
            reply = "Hmm 🤍 thoda aur batao na"

        await update.message.reply_text(reply)

    except Exception as e:
        logging.error(e)
        await update.message.reply_text(
            "Abhi thoda issue aa gaya 😕 phir se bolo na"
        )

# ---------- MAIN ----------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("Basanti is running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
