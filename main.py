import os
import re
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)
from ai_engine import ask_ai

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hii 🙂 Main Basanti hoon 🌸")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    chat = update.effective_chat
    text = msg.text or ""

    # Group rule: reply only on mention or reply-to-bot
    if chat.type in ["group", "supergroup"]:
        bot_u = context.bot.username
        is_mention = f"@{bot_u}".lower() in text.lower()
        is_reply = (
            msg.reply_to_message
            and msg.reply_to_message.from_user
            and msg.reply_to_message.from_user.is_bot
        )
        if not is_mention and not is_reply:
            return
        if is_mention:
            text = re.sub(f"@{bot_u}", "", text, flags=re.I).strip()

    messages = [{"role": "user", "content": text}]
    try:
        reply = ask_ai(messages)
    except Exception:
        reply = "Abhi thoda sa issue aa gaya 🙂 thodi der baad try karo."

    await msg.reply_text(reply)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Basanti running (ChatGPT-style)")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
