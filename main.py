import os
import asyncio
import requests
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from memory import save_message, get_memory

# ===== ENV =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-4o-mini"

SYSTEM_PROMPT = (
    "You are Basanti AI, a smart, friendly, human-like assistant. "
    "You speak Hindi and English naturally. "
    "In groups, you reply only when mentioned or replied to. "
    "Never spam. Be respectful, helpful, and calm."
)

# ===== AI CALL =====
def ask_ai(user_id, user_text):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(get_memory(user_id))
    messages.append({"role": "user", "content": user_text})

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://railway.app",
        "X-Title": "Basanti AI Bot"
    }

    payload = {
        "model": MODEL,
        "messages": messages
    }

    r = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload,
        timeout=60
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

# ===== COMMANDS =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Namaste! Main *Basanti AI* hoon.\n"
        "Mujhse Hindi ya English me baat kar sakte ho 🙂",
        parse_mode="Markdown"
    )

# ===== MAIN MESSAGE HANDLER =====
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    text = message.text or ""
    chat = update.effective_chat
    user_id = message.from_user.id

    # ===== GROUP STRICT LOGIC =====
    if chat.type in ["group", "supergroup"]:
        mentioned = (
            context.bot.username
            and f"@{context.bot.username.lower()}" in text.lower()
        )

        replied_to_bot = (
            message.reply_to_message
            and message.reply_to_message.from_user
            and message.reply_to_message.from_user.id == context.bot.id
        )

        if not (mentioned or replied_to_bot):
            return  # 🚫 ignore normal group messages

    # ===== SAVE USER MESSAGE =====
    save_message(user_id, "user", text)

    # ===== TYPING EFFECT (WhatsApp feel) =====
    await context.bot.send_chat_action(
        chat_id=chat.id,
        action=ChatAction.TYPING
    )
    await asyncio.sleep(2)

    # ===== AI RESPONSE =====
    try:
        reply = ask_ai(user_id, text)
    except Exception:
        reply = "😕 Thoda issue aa gaya, thodi der baad try karo."

    save_message(user_id, "assistant", reply)
    await message.reply_text(reply)

# ===== RUN =====
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ BASANTI AI BOT STARTED")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
