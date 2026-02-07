from telegram import Update
from teimport os
import asyncio
import time
import re
import requests
from collections import defaultdict, deque

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from memory import save_short, save_long, get_short, get_long

# ================== ENV ==================
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-4o-mini"

# ================== ADMIN SETTINGS ==================
FLOOD_LIMIT = 5          # messages
FLOOD_TIME = 10          # seconds
WARN_LIMIT = 1           # warnings before mute
MUTE_TIME = 60           # seconds

# ================== STATE ==================
user_messages = defaultdict(lambda: deque())
user_warnings = defaultdict(int)
welcomed_users = set()

# ================== UTILS ==================
LOW_EFFORT = re.compile(r"^(ok|okay|hmm+|👍|😂|yes|no)$", re.I)
ABUSE_WORDS = ["idiot", "stupid", "hate", "pagal", "gadha"]

def detect_mood(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["sad", "tired", "lonely"]):
        return "sad"
    if any(w in t for w in ABUSE_WORDS):
        return "angry"
    if "?" in t or "help" in t:
        return "confused"
    if any(w in t for w in ["happy", "great", "good"]):
        return "happy"
    return "neutral"

def system_prompt(mood: str) -> str:
    base = (
        "You are Basanti AI — calm, respectful, romantic-but-decent, "
        "and a responsible group admin. "
        "You never spam. You speak Hindi-English naturally."
    )
    if mood == "angry":
        return base + " Calm the situation politely. De-escalate."
    if mood == "sad":
        return base + " Be soft, caring, and supportive."
    if mood == "confused":
        return base + " Explain step-by-step clearly."
    if mood == "happy":
        return base + " Be warm and friendly."
    return base

def ask_ai(user_id, text, mood):
    messages = [
        {
            "role": "system",
            "content": (
                "You are Basanti AI. "
                "Never repeat the user's message. "
                "Never say 'Tumne bola' or 'You said'. "
                "Reply naturally like a human chat."
            )
        }
    ]

    # long-term memory
    facts = get_long(user_id)
    if facts:
        messages.append({
            "role": "system",
            "content": "User info:\n" + "\n".join(facts)
        })

    # short-term memory (clean)
    for m in get_short(user_id):
        if m["role"] == "user":
            messages.append({"role": "user", "content": m["content"]})
        elif m["role"] == "assistant":
            messages.append({"role": "assistant", "content": m["content"]})

    # CURRENT USER MESSAGE (NO PREFIX)
    messages.append({
        "role": "user",
        "content": text
    })

    r = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": messages,
            "temperature": 0.7
        },
        timeout=60
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]
# ================== COMMANDS ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 *Basanti AI Admin Active*\n"
        "Main group ko pyar aur discipline dono se sambhalti hoon 🌸",
        parse_mode="Markdown"
    )

# ================== WELCOME ==================
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.id in welcomed_users:
            continue
        welcomed_users.add(member.id)
        await update.message.reply_text(
            f"🌸 Welcome {member.mention_html()}!\n"
            "Group rules pinned hain — aaram se baat karein 😊",
            parse_mode="HTML"
        )

# ================== MAIN HANDLER ==================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    chat = update.effective_chat
    user = message.from_user
    text = (message.text or "").strip()

    if not text or LOW_EFFORT.match(text):
        return

    # -------- FLOOD CONTROL --------
    now = time.time()
    q = user_messages[user.id]
    q.append(now)
    while q and now - q[0] > FLOOD_TIME:
        q.popleft()

    if len(q) > FLOOD_LIMIT:
        user_warnings[user.id] += 1
        if user_warnings[user.id] > WARN_LIMIT:
            await context.bot.restrict_chat_member(
                chat.id,
                user.id,
                permissions=None,
                until_date=now + MUTE_TIME
            )
            await message.reply_text(
                f"⛔ {user.first_name}, thoda break lo.\n"
                "Group ka mahaul shant rakhen 🙏"
            )
        else:
            await message.reply_text(
                f"⚠️ {user.first_name}, thoda slow rakhein.\n"
                "Sabko bolne ka mauka mile 🌿"
            )
        return

    # -------- ABUSE CONTROL --------
    if any(w in text.lower() for w in ABUSE_WORDS):
        await message.reply_text(
            "🕊️ Shant rahiye.\n"
            "Baat ko personal na banayein 🙏"
        )
        return

    # -------- GROUP STRICT RULE --------
    if chat.type in ["group", "supergroup"]:
        mentioned = context.bot.username and f"@{context.bot.username.lower()}" in text.lower()
        replied = (
            message.reply_to_message
            and message.reply_to_message.from_user
            and message.reply_to_message.from_user.id == context.bot.id
        )
        if not (mentioned or replied):
            return

    # -------- MEMORY --------
    save_short(user.id, "user", text)
    if "my name is" in text.lower():
        save_long(user.id, "name", text.split("is", 1)[-1].strip())

    mood = detect_mood(text)

    await context.bot.send_chat_action(chat.id, ChatAction.TYPING)
    await asyncio.sleep(2)

    try:
        reply = ask_ai(user.id, text, mood)
    except Exception:
        reply = "😕 Thodi dikkat aa rahi hai, baad me try karein."

    save_short(user.id, "assistant", reply)
    await message.reply_text(reply)

# ================== RUN ==================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ BASANTI AI — ADMIN GOD MODE (PHASE-1) ACTIVE")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
