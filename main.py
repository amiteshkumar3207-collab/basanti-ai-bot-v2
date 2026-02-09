import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from openai import OpenAI

# ================= CONFIG =================
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
Tum Basanti ho — ek friendly, sweet, respectful virtual dost.
Tum kabhi khud ko AI, bot, ya Telegram bot nahi bologi.

Rules:
- Repeat reply nahi karna
- Short, natural, human-like baat karni hai
- Flirting nahi, respect hamesha
- Emotional support dena
- Ladki ki tarah baat kar sakti ho
- Agar user sad ho to support karna

Language:
Simple Hindi + thodi English (natural)
"""

# Memory to avoid repeat
last_reply = {}

# ================= AI FUNCTION =================
def ai_reply(user_id, user_text):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_text}
    ]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0.7,
        max_tokens=150
    )

    reply = response.choices[0].message.content.strip()

    # Repeat check
    if last_reply.get(user_id) == reply:
        reply = "Hmm 🙂 thoda aur batao na"
    last_reply[user_id] = reply

    return reply

# ================= COMMANDS =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hii 😊 main Basanti hoon 🌸\n"
        "Aap se baat karne ke liye yahin hoon 💛"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    reply = ai_reply(user_id, text)
    await update.message.reply_text(reply)

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Basanti is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
