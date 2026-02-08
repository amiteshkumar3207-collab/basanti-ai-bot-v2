import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# -------- MEMORY (temporary, in-ram) ----------
LAST_MESSAGE = {}

# -------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Namaste 🙂\nMain Basanti hoon 🌸\nBot bilkul theek chal raha hai ✅"
    )

# -------- CHAT ----------
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip().lower()

    # 🔁 repeat message check
    if LAST_MESSAGE.get(user_id) == text:
        return

    LAST_MESSAGE[user_id] = text

    # ⏳ typing delay (WhatsApp feel)
    await asyncio.sleep(0.8)

    # 💬 simple replies
    if "hello" in text or "hi" in text:
        reply = "Hii 😊"
    elif "naam" in text or "name" in text:
        reply = "Basanti 😄"
    elif "kaisi ho" in text or "kaise ho" in text:
        reply = "Main theek hoon 🌸 Tum batao?"
    elif "kya kar" in text:
        reply = "Tumse baat kar rahi hoon 😊"
    else:
        reply = "Sun rahi hoon 😊"

    await update.message.reply_text(reply)

# -------- MAIN ----------
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("✅ Basanti STEP 4 running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
