from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
import os
import requests

# ENV VARIABLES
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# SYSTEM PROMPT
SYSTEM_PROMPT = """
You are Basanti, a good-natured, calm, and helpful AI.
You speak Hindi, English, and Hinglish naturally.
Reply briefly, clearly, and politely.
"""

# AI FUNCTION
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

# /start COMMAND
async def start(update, context):
    await update.message.reply_text(
        "🌼 Main Basanti hoon.\nGroup me mujhe @mention karke poochho 🙂"
    )

# GROUP REPLY (ONLY ON MENTION)
async def group_reply(update, context):
    message = update.message
    if not message or not message.text:
        return

    text = message.text
    bot_username = context.bot.username

    # Agar bot mention nahi hua
    if f"@{bot_username}" not in text:
        return

    # Mention hata ke clean question
    clean_text = text.replace(f"@{bot_username}", "").strip()

    if not clean_text:
        await message.reply_text("🌼 Haan? Aap kya poochna chahte ho 🙂")
        return

    answer = ask_ai(clean_text)
    await message.reply_text(answer)

# APP START
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, group_reply))
app.run_polling()
