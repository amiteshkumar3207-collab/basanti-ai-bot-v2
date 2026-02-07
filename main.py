import os
import asyncio
import requests
import re
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

# ===== ENV =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-4o-mini"

# ===== SILENCE RULES =====
LOW_EFFORT_PATTERNS = re.compile(
    r"^(ok|okay|hmm+|hm+|👍|👌|😂|🤣|😅|😐|yes|no|k|thx|thanks)$",
    re.IGNORECASE
)

# ===== MOOD DETECTION =====
def detect_mood(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["sad", "depressed", "down", "cry", "tired", "lonely"]):
        return "sad"
    if any(w in t for w in ["angry", "mad", "furious", "hate", "stupid", "idiot"]):
        return "angry"
    if any(w in t for w in ["confused", "how", "why", "what", "help", "?"]):
        return "confused"
    if any(w in t for w in ["happy", "great", "awesome", "good news", "yay"]):
        return "happy"
    return "neutral"

def system_prompt_for_mood(mood: str) -> str:
    base = (
        "You are Basanti AI, a highly intelligent, human-like assistant. "
        "You speak Hindi and English naturally. "
        "You NEVER spam. "
        "In groups, you reply only when mentioned or replied to. "
        "Be respectful, calm, and helpful."
    )
    if mood == "sad":
        return base + " User is sad. Be empathetic, soft, and supportive."
    if mood == "angry":
        return base + " User is angry. Be calm, short, de-escalate politely."
    if mood == "confused":
        return base + " User is confused. Explain step-by-step, clearly."
    if mood == "happy":
        return base + " User is happy. Be friendly and encouraging."
    return base + " Keep tone neutral and concise."

# ===== AI CALL =====
def ask_ai(user_id, user_text, mood):
    messages = [{"role": "system", "content": system_prompt_for_mood(mood)}]

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

# ===== COMMANDS =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Namaste! Main *Basanti AI* hoon.\n"
        "Main aapka mood samajh kar reply karti hoon 🙂",
        parse_mode="Markdown"
    )

# ===== MAIN HANDLER =====
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    text = (message.text or "").strip()
    chat = update.effective_chat
    user = message.from_user

    # ---- SMART SILENCE: low-effort messages ----
    if LOW_EFFORT_PATTERNS.match(text):
        return

    # ---- GROUP STRICT LOGIC ----
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

    # ---- SHORT MEMORY ----
    save_short(user.id, "user", text)

    # ---- SIMPLE LONG-TERM EXTRACTION ----
    low = text.lower()
    if "my name is" in low:
        name = text.split("is", 1)[-1].strip()
        if name:
            save_long(user.id, "name", name)
    if "i want to" in low or "my goal" in low:
        save_long(user.id, "goal", text)

    # ---- MOOD ----
    mood = detect_mood(text)

    # ---- TYPING (human feel) ----
    await context.bot.send_chat_action(chat.id, ChatAction.TYPING)
    await asyncio.sleep(2)

    # ---- AI REPLY ----
    try:
        reply = ask_ai(user.id, text, mood)
    except Exception:
        reply = "😕 Thoda issue aa gaya, thodi der baad try karo."

    save_short(user.id, "assistant", reply)
    await message.reply_text(reply)

# ===== RUN =====
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ BASANTI AI — LAYER-B (MOOD & SILENCE) ACTIVE")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
