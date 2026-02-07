
# main.py
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

# ========== ENV VARIABLES ==========
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "openai/gpt-3.5-turbo"   # free-friendly & stable

# ========== AI ENGINE ==========
def ask_ai(system_prompt, messages):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            *messages
        ]
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
    data = response.json()

    return data["choices"][0]["message"]["content"]


# ========== START COMMAND ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Namaste 😊\nMain **Basanti** hoon 🌸\nPyaar se baat karne wali AI bot 🤖❤️"
    await update.message.reply_text(text)


# ========== MAIN MESSAGE HANDLER ==========
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    chat = update.effective_chat
    user = update.effective_user

    user_id = user.id
    user_text = message.text

    # ---------- GROUP LOGIC ----------
    if chat.type in ["group", "supergroup"]:
        bot_username = context.bot.username
        if f"@{bot_username}" not in user_text:
            return  # ignore if not mentioned

        # remove mention from text
        user_text = user_text.replace(f"@{bot_username}", "").strip()

    # ---------- MEMORY SAVE ----------
    save_message(user_id, "user", user_text)

    # ---------- CONTEXT ----------
    context_messages = get_context(user_id)

    ai_messages = []
    for msg in context_messages:
        ai_messages.append({
            "role": msg["role"],
            "content": msg["text"]
        })

    # ---------- AI CALL ----------
    system_prompt = get_system_prompt()

    try:
        reply = ask_ai(system_prompt, ai_messages)
    except Exception as e:
        reply = "Thoda sa issue aa gaya 😔\nThodi der baad try karo."

    # ---------- SAVE BOT REPLY ----------
    save_message(user_id, "bot", reply)

    await message.reply_text(reply)


# ========== MAIN ==========
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Basanti is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
