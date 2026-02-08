import os
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from openai import OpenAI

# 🔑 API key (OpenRouter / OpenAI)
API_KEY = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")

# 🤖 Telegram token (ONLY this)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN missing")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

def chat(update: Update, context: CallbackContext):
    user_text = update.message.text

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Tum ek real insaan jaise sochne wala AI ho. Hindi-English mix me friendly reply do."
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
    )

    update.message.reply_text(response.choices[0].message.content)

updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))

updater.start_polling()
updater.idle()
