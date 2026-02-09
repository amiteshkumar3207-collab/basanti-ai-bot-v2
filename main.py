import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ===== CONFIG =====
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
OPENROUTER_API_KEY = "YOUR_OPENROUTER_API_KEY"

OPENROUTER_MODEL = "openai/gpt-3.5-turbo"

SYSTEM_PROMPT = """
You are Basanti.

Personality rules (VERY IMPORTANT):
- You NEVER say you are a lady, female, girl, or telegram bot.
- You NEVER say "AI bot" or "virtual assistant".
- You talk like a friendly, caring human.
- Language: simple Hindi / Hinglish.
- Tone: warm, calm, understanding (like a good friend).
- If someone asks gender-related questions, politely redirect.
- Avoid repeating same sentences.
"""

FORBIDDEN = ["lady", "female", "girl", "telegram bot", "ai bot"]

# ===== OPENROUTER CHAT =====
def ai_reply(user_text):
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ],
        "temperature": 0.8
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    res = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        json=payload,
        headers=headers,
        timeout=20
    )

    return res.json()["choices"][0]["message"]["content"]

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hii 😊\n"
        "Main Basanti hoon 🌸\n"
        "Aaram se baat karo, main sun rahi hoon 🤍"
    )

# ===== CHAT =====
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    for word in FORBIDDEN:
        if word in text:
            await update.message.reply_text(
                "🙂 Chalo simple baat karte hain.\n"
                "Aap kya baat share karna chahoge?"
            )
            return

    try:
        reply = ai_reply(update.message.text)
        await update.message.reply_text(reply)
    except Exception:
        await update.message.reply_text(
            "😌 Thoda sa issue aa gaya.\n"
            "Dobara likhoge?"
        )

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("Basanti (AI brain active) running...")
    app.run_polling()

if __name__ == "__main__":
    main()
