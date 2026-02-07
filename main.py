from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

BOT_USERNAME = "@BasantiBot"   # 👈 yahan apna exact bot username daalo

SYSTEM_PROMPT = """
You are Basanti, a good-natured, calm, and helpful AI.
You speak Hindi, English, and Hinglish naturally.
Reply briefly, clearly, and politely.
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
    await update.message.reply_text("🌼 Basanti ready hoon. Group me mujhe tag karke poochho 🙂")

async def group_reply(update, context):
    message = update.message
    text = message.text

    # ❌ Agar text hi nahi hai
    if not text:
        return

    # ❌ Agar bot mention nahi hai
    if BOT_USERNAME.lower() not in text.lower():
        return

    # Mention hata ke clean question nikalo
    clean_text = text.replace(BOT_USERNAME, "").strip()

    if not clean_text:
        await message.reply_text("🌼 Haan? Aap kya poochna chahte ho 🙂")
        return

    answer = ask_ai(clean_text)
    await message.reply_text(answer)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, group_reply))

app.run_polling()
