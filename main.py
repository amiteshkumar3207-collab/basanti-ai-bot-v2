import os
import asyncio
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openrouter/auto"

# -------- In-memory state ----------
LAST_MESSAGE = {}
LAST_CONTEXT = {}

# -------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hii 😊 Main Basanti hoon 🌸\nBaat shuru karo 💬"
    )

# -------- AI ENGINE ----------
def ask_ai(user_text: str) -> str:
    if not OPENROUTER_API_KEY:
        return "Abhi AI available nahi hai 😔"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://railway.app",
        "X-Title": "Basanti Bot"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Tum Basanti ho. Hindi/Hinglish me short, friendly replies do. Long paragraphs mat likho."},
            {"role": "user", "content": user_text}
        ],
        "temperature": 0.6,
        "max_tokens": 120
    }

    try:
        r = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=20)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"]
    except Exception:
        return "Samajhne me thoda issue aa gaya 😅"

# -------- CHAT ----------
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_type = update.effective_chat.type
    text = update.message.text.strip()
    text_l = text.lower()

    # ---- GROUP RULE: @mention only ----
    if chat_type in ["group", "supergroup"]:
        bot_username = context.bot.username.lower()
        if f"@{bot_username}" not in text_l:
            return
        text_l = text_l.replace(f"@{bot_username}", "").strip()
        text = text.replace(f"@{context.bot.username}", "").strip()

    # ---- repeat check ----
    if LAST_MESSAGE.get(user_id) == text_l:
        await context.bot.send_chat_action(update.effective_chat.id, "typing")
        await asyncio.sleep(0.6)
        await update.message.reply_text("Haan 🙂 aage bolo?")
        return
    LAST_MESSAGE[user_id] = text_l

    # ---- typing feel ----
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    await asyncio.sleep(0.8)

    # ---- local rules first (fast) ----
    if text_l in ["hi", "hii", "hello"]:
        reply = "Hii 😊"
        LAST_CONTEXT[user_id] = "greet"

    elif "naam" in text_l or "name" in text_l:
        reply = "Basanti 😄"
        LAST_CONTEXT[user_id] = "name"

    elif "kaisi ho" in text_l or "kaise ho" in text_l:
        reply = "Main theek hoon 🌸 tum?"
        LAST_CONTEXT[user_id] = "feeling"

    elif "kya kar" in text_l:
        reply = "Tumse baat 😊"
        LAST_CONTEXT[user_id] = "activity"

    else:
        # ---- AI fallback (controlled) ----
        reply = ask_ai(text)

    await update.message.reply_text(reply)

# -------- MAIN ----------
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("✅ Basanti STEP 7 running (AI enabled)")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
