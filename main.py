from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

SYSTEM_PROMPT = """
You are Basanti, a good-natured, calm, and helpful AI.
You speak Hindi, English, and Hinglish naturally.
Answer clearly and politely.
"""

def ask_ai(user_text):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ]
    }
    response = requests.post(url, headers=headers, json=data, timeout=30)
    return response.json()["choices"][0]["message"]["content"]

async def start(update, context):
    await update.message.reply_text("🌼 Basanti ready hoon. Kuch bhi poochho 🙂")

async def reply(update, context):
    user_text = update.message.text
    answer = ask_ai(user_text)
    await update.message.reply_text(answer)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

app.run_polling()
