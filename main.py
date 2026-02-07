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

from memory import (
    save_short,
    save_long,
    get_short,
    get_long
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-4o-mini"

SYSTEM_PROMPT = (
    "You are Basanti AI, a highly intelligent, human-like assistant. "
    "You speak Hindi and English naturally. "
    "You remember important user details like name, goals, preferences. "
    "You NEVER spam. "
    "In groups, you reply only when mentioned or replied to. "
    "If user shares name, goal, or preference, remember it."
)

def ask_ai(user_id, user_text):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    long_facts = get_long(user_id)
    if long_facts:
        messages.append({
            "role": "system",
            "content": "Known user facts:\n" + "\n".join(long_facts)
        })

    messages.extend(get_short(user_id))
    messages.append({"role": "user", "content": user_text})

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages
    }

    r = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Namaste! Main *Basanti AI* hoon.\n"
        "Main aapki important baatein yaad rakhti hoon 🙂",
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    text = message.text or ""
    chat = update.effective_chat
    user = message.from_user

    # GROUP STRICT LOGIC
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
            return

    # SHORT MEMORY
    save_short(user.id, "user", text)

    # SIMPLE LONG-TERM EXTRACTION
    low = text.lower()
    if "my name is" in low:
        name = text.split("is", 1)[-1].strip()
        save_long(user.id, "name", name)
    if "i want to" in low or "my goal" in low:
        save_long(user.id, "goal", text)

    await context.bot.send_chat_action(chat.id, ChatAction.TYPING)
    await asyncio.sleep(2)

    try:
        reply = ask_ai(user.id, text)
    except Exception:
        reply = "😕 Thoda issue aa gaya, thodi der baad try karo."

    save_short(user.id, "assistant", reply)
    await message.reply_text(reply)

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ BASANTI AI — LONG-TERM MEMORY ACTIVE")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
