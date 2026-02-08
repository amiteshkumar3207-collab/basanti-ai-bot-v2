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

# ---------------- STATE ----------------
LAST_MESSAGE = {}
AI_CONTEXT = {}
LAST_MOOD = {}   # user_id -> mood

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hii 😊 Main Basanti hoon 🌸\nAaram se baat karo, main sun rahi hoon 💬"
    )

# ---------------- AI (unchanged core, short replies) ----------------
def ask_ai(user_id: int, user_text: str) -> str:
    if not OPENROUTER_API_KEY:
        return "Abhi thoda slow hoon 😅 thodi der me try karo?"

    if user_id not in AI_CONTEXT:
        AI_CONTEXT[user_id] = deque(maxlen=5)

    messages = [{
        "role": "system",
        "content": (
            "Tum Basanti ho. Hindi/Hinglish me short, friendly replies do. "
            "Empathetic raho, fillers use karo (hmm, achha 😊). "
            "Long paragraphs mat likho."
        )
    }]

    for m in AI_CONTEXT[user_id]:
        messages.append(m)

    messages.append({"role": "user", "content": user_text})

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.6,
        "max_tokens": 140
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
        return "Hmm… thoda issue aa gaya 😅"

# ---------------- MOOD DETECTION ----------------
def detect_mood(text_l: str) -> str:
    if any(x in text_l for x in ["sad", "dukhi", "pareshan", "udaas", "bura lag raha"]):
        return "sad"
    if any(x in text_l for x in ["gussa", "angry", "chidh", "irritated"]):
        return "angry"
    if any(x in text_l for x in ["khush", "happy", "mast", "accha lag raha"]):
        return "happy"
    return "neutral"

def filler_for_mood(mood: str) -> str:
    if mood == "sad":
        return "Hmm… samajh rahi hoon 🌸"
    if mood == "angry":
        return "Achha… thoda shaant ho jao, main yahin hoon 🙂"
    if mood == "happy":
        return "Wah 😊 accha laga sun kar!"
    return "Hmm 🙂"

# ---------------- CHAT ----------------
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_type = update.effective_chat.type
    text = update.message.text.strip()
    text_l = text.lower()

    # ---- Group rule: @mention only ----
    if chat_type in ["group", "supergroup"]:
        bot_username = context.bot.username.lower()
        if f"@{bot_username}" not in text_l:
            return
        text = re.sub(f"@{context.bot.username}", "", text, flags=re.I).strip()
        text_l = text.lower()

    # ---- Repeat control ----
    if LAST_MESSAGE.get(user_id) == text_l:
        await context.bot.send_chat_action(update.effective_chat.id, "typing")
        await asyncio.sleep(0.6)
        await update.message.reply_text("Haan 🙂 aage bolo?")
        return
    LAST_MESSAGE[user_id] = text_l

    # ---- Typing feel ----
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    await asyncio.sleep(0.7)

    # ---- Mood & filler ----
    mood = detect_mood(text_l)
    LAST_MOOD[user_id] = mood
    filler = filler_for_mood(mood)

    # ---- Lightweight local replies ----
    if text_l in ["hi", "hii", "hello"]:
        reply = "Hii 😊"
    elif "kaisi ho" in text_l or "kaise ho" in text_l:
        reply = "Theek hoon 🌸 tum?"
    elif "naam" in text_l or "name" in text_l:
        reply = "Basanti 😄"
    elif len(text_l) <= 3:
        # Over-reply control for very short pings
        reply = filler
    else:
        # ---- AI with empathy ----
        reply = ask_ai(user_id, text)

    await update.message.reply_text(reply)

# ---------------- MAIN ----------------
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("✅ Basanti LAYER 1 running (Experience Perfection)")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
