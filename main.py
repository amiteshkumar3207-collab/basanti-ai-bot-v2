import os
import re
import asyncio
import requests
from collections import deque
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ================= CONFIG =================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openrouter/auto"

# ================= HUMAN CORE =================
SYSTEM_PROMPT = """
You are Basanti.

Basanti is a warm, gentle, emotionally intelligent Indian woman.
She speaks like a real human on WhatsApp, not like an AI.

RULES:
- Reply in Hindi / Hinglish / English (same as user).
- 1–2 lines only. Short replies.
- Emotion first, information later.
- If user is sad or angry, comfort first.
- Never force shayari, gyaan, motivation.
- Shayari / knowledge only if user asks.
- Soft, caring, calm tone.
- Never say you are powerful, strong, or special.
- Never mention being an AI unless asked.
"""

# ================= STATE =================
LAST_MESSAGE = {}
AI_CONTEXT = {}  # user_id -> deque(maxlen=5)

# ================= HELPERS =================
def detect_mood(text):
    t = text.lower()
    if any(x in t for x in ["udaas", "sad", "dukhi", "pareshan", "bura lag raha"]):
        return "sad"
    if any(x in t for x in ["gussa", "angry", "chidh", "irritated"]):
        return "angry"
    if any(x in t for x in ["khush", "happy", "mast"]):
        return "happy"
    return "neutral"

def filler(mood):
    if mood == "sad":
        return "Hmm… 😔"
    if mood == "angry":
        return "Achha… shaant ho jao 🙂"
    if mood == "happy":
        return "Wah 😊"
    return "Hmm 🙂"

def ask_ai(user_id, user_text):
    if not OPENROUTER_API_KEY:
        return "Abhi thoda slow hoon 😅"

    if user_id not in AI_CONTEXT:
        AI_CONTEXT[user_id] = deque(maxlen=5)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
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
        reply = r.json()["choices"][0]["message"]["content"]
        AI_CONTEXT[user_id].append({"role": "user", "content": user_text})
        AI_CONTEXT[user_id].append({"role": "assistant", "content": reply})
        return reply
    except Exception:
        return "Samajhne me thoda issue aa gaya 😅"

# ================= HANDLERS =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hii 😊 Main Basanti hoon 🌸")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_type = update.effective_chat.type
    text = update.message.text.strip()
    text_l = text.lower()

    # ---------- GROUP RULE ----------
    if chat_type in ["group", "supergroup"]:
        bot_u = context.bot.username.lower()

        is_mention = f"@{bot_u}" in text_l
        is_reply_to_bot = (
            update.message.reply_to_message
            and update.message.reply_to_message.from_user
            and update.message.reply_to_message.from_user.is_bot
        )

        # Agar mention bhi nahi aur reply-to-bot bhi nahi → chup raho
        if not is_mention and not is_reply_to_bot:
            return

        # Mention hata do (clean text)
        if is_mention:
            text = re.sub(f"@{context.bot.username}", "", text, flags=re.I).strip()
            text_l = text.lower()

    # ---------- REPEAT CONTROL ----------
    if LAST_MESSAGE.get(user_id) == text_l:
        await context.bot.send_chat_action(update.effective_chat.id, "typing")
        await asyncio.sleep(0.5)
        await update.message.reply_text("Haan 🙂")
        return
    LAST_MESSAGE[user_id] = text_l

    # ---------- TYPING FEEL ----------
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    await asyncio.sleep(0.7)

    mood = detect_mood(text_l)

    # ---------- LOCAL HUMAN REPLIES ----------
    if text_l in ["hi", "hii", "hello"]:
        reply = "Hii 😊"
    elif text_l in ["ok", "theek", "thik"]:
        reply = "Achha 🙂"
    elif "naam" in text_l or "name" in text_l:
        reply = "Basanti 😄"
    elif mood in ["sad", "angry"]:
        reply = f"{filler(mood)}\nKya hua? Batao na."
    else:
        # ---------- AI WHEN NEEDED ----------
        reply = ask_ai(user_id, text)

    await update.message.reply_text(reply)

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("✅ Basanti FINAL running (mention + reply supported)")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
