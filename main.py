import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from openai import OpenAI

# ===== CONFIG =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
Tum Basanti ho — ek pyari, samajhdar virtual dost.
Tum khud ko AI, bot, ya Telegram bot nahi bologi.

Rules:
- Repeat jawab nahi
- Short, natural Hindi replies
- Emotional support dena
- Respectful & friendly rehna
- Flirt ya adult baat nahi
"""

# ===== AI FUNCTION =====
def ai_reply(user_text):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ],
        temperature=0.8,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

# ===== HANDLERS =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hii 😊 main Basanti hoon 🌸\nAapse baat karne ke liye yahin hoon 💛"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        reply = ai_reply(user_text)
    except Exception as e:
        reply = "Thoda sa issue aa gaya 😔, fir se likho na"

    await update.message.reply_text(reply)

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    app.run_polling()

if __name__ == "__main__":
    main()
