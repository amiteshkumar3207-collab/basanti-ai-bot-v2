import os
import asyncio
import requests
import re
from collections import deque
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

# ---------------- MEMORY ----------------
LAST_MESSAGE = {}
AI_CONTEXT = {}

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hii 😊 Main **Basanti** hoon 🌸\n"
        "Shayari 💐 | Math 🧮 | Knowledge 📚\n"
        "Bolo, kya chahiye?"
    )

# ---------------- AI ENGINE ----------------
def ask_ai(user_id: int, user_text: str) -> str:
    if not OPENROUTER_API_KEY:
        return "Abhi AI available nahi hai 😔"

    if user_id not in AI_CONTEXT:
        AI_CONTEXT[user_id] = deque(maxlen=5)

    messages = [
        {
            "role": "system",
            "content": (
                "Tum Basanti ho. Ek pyari ladki. "
                "Hindi/Hinglish me short, friendly replies do. "
                "Shayari aur ghazal achhi aati hai."
            )
        }
    ]

    for m in AI_CONTEXT[user_id]:
        messages.append(m)

    messages.append({"role": "user", "content": user_text})

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 180
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=20)
        r.raise_for_status()
        data = r.json()
        reply = data["choices"][0]["message"]["content"]

        AI_CONTEXT[user_id].append({"role": "user", "content": user_text})
        AI_CONTEXT[user_id].append({"role": "assistant", "content": reply})

        return reply
    except Exception:
        return "Samajhne me thoda issue aa gaya 😅"

# ---------------- CHAT ----------------
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_type = update.effective_chat.type
    text = update.message.text.strip()
    text_l = text.lower()

    # -------- Group rule: mention only --------
    if chat_type in ["group", "supergroup"]:
        bot_username = context.bot.username.lower()
        if f"@{bot_username}" not in text_l:
            return
        text = re.sub(f"@{context.bot.username}", "", text, flags=re.I).strip()
        text_l = text.lower()

    # -------- Repeat check --------
    if LAST_MESSAGE.get(user_id) == text_l:
        await context.bot.send_chat_action(update.effective_chat.id, "typing")
        await asyncio.sleep(0.5)
        await update.message.reply_text("Haan 😊 aage bolo?")
        return
    LAST_MESSAGE[user_id] = text_l

    # -------- Typing feel --------
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    await asyncio.sleep(0.8)

    # -------- TALENTS --------

    # 🌸 Shayari / Ghazal
    if any(x in text_l for x in ["shayari", "शायरी", "ghazal", "ग़ज़ल"]):
        reply = ask_ai(user_id, f"Ek pyari si shayari likho: {text}")

    # 🧮 Math (simple)
    elif re.fullmatch(r"[0-9\+\-\*/\(\)\s\.]+", text):
        try:
            result = eval(text)
            reply = f"🧮 Answer: {result}"
        except Exception:
            reply = "Math thoda galat lag raha hai 😅"

    # 💬 Casual chat
    elif text_l in ["hi", "hii", "hello"]:
        reply = "Hii 😊"
    elif "kaisi ho" in text_l:
        reply = "Main theek hoon 🌸 tum?"

    # 📚 Knowledge / AI fallback
    else:
        reply = ask_ai(user_id, text)

    await update.message.reply_text(reply)

# ---------------- MAIN ----------------
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("✅ Basanti TALENTS running")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
