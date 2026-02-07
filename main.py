import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "qwen/qwen3-80b-instruct:free"


def should_reply(update: Update) -> bool:
    message = update.message

    # Private chat → always reply
    if message.chat.type == "private":
        return True

    # Group logic
    if message.chat.type in ["group", "supergroup"]:
        # Reply to bot
        if message.reply_to_message and message.reply_to_message.from_user.is_bot:
            return True

        # Mention bot
        if message.entities:
            for ent in message.entities:
                if ent.type == "mention":
                    return True

    return False


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not should_reply(update):
        return

    user_text = update.message.text

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://t.me/your_bot",
        "X-Title": "Basanti AI Bot"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Basanti AI — smart, friendly, human-like assistant. "
                    "Reply naturally in Hindi or English depending on user."
                )
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
    }

    try:
        r = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)
        r.raise_for_status()
        reply = r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        reply = "⚠️ Thoda issue aaya hai, dobara try karo."

    await update.message.reply_text(reply)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
