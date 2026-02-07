import os
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from memory import save_message, get_context
from personality import get_system_prompt

# ========= ENV =========
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "openrouter/auto"

# ========= AI =========
def ask_ai(system_prompt, messages):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://railway.app",
        "X-Title": "Basanti Telegram Bot"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            *messages
        ],
        "temperature": 0.7
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload,
        timeout=30
    )

    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]

# ========= START =========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Namaste 😊\nMain **Basanti** hoon 🌸\nPyaar se baat karne wali AI bot 🤖❤️"
    )

# ========= MESSAGE =========
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    chat = update.effective_chat
    user = update.effective_user

    user_text = message.text
    user_id = user.id

    if chat.type in ["group", "supergroup"]:
        bot_username = context.bot.username
        if f"@{bot_username}" not in user_text:
            return
        user_text = user_text.replace(f"@{bot_username}", "").strip()

    save_message(user_id, "user", user_text)
    history = get_context(user_id)

    ai_messages = [
        {"role": m["role"], "content": m["text"]}
        for m in history
    ]

    try:
        reply = ask_ai(get_system_prompt(), ai_messages)
    except Exception as e:
        print("AI ERROR:", e)
        reply = "Basanti thodi confused ho gayi 😅\nThodi der baad try karo."

    save_message(user_id, "bot", reply)
    await message.reply_text(reply)

# ========= MAIN =========
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Basanti is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
