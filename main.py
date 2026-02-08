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

# -------- In-memory context (STEP 5) ----------
LAST_MESSAGE = {}
LAST_CONTEXT = {}

# -------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Namaste 🙂\nMain Basanti hoon 🌸\nBaat shuru karo 💬"
    )

# -------- CHAT ----------
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip().lower()

    # Ignore exact repeat messages
    if LAST_MESSAGE.get(user_id) == text:
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action="typing"
        )
        await asyncio.sleep(0.6)
        await update.message.reply_text("Haan, wahi 🙂 bolo aage?")
        return

    LAST_MESSAGE[user_id] = text

    # Typing indicator (WhatsApp feel)
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )
    await asyncio.sleep(0.8)

    # -------- Intent detection ----------
    if any(x in text for x in ["hi", "hello", "hii"]):
        reply = "Hii 😊"
        LAST_CONTEXT[user_id] = "greeting"

    elif "naam" in text or "name" in text:
        reply = "Basanti 😄"
        LAST_CONTEXT[user_id] = "name"

    elif "kaisi ho" in text or "kaise ho" in text:
        # Follow-up if same context
        if LAST_CONTEXT.get(user_id) == "feeling":
            reply = "Abhi bhi theek hoon 🌸 tum sunao?"
        else:
            reply = "Main theek hoon 🌸 tum?"
        LAST_CONTEXT[user_id] = "feeling"

    elif "kya kar" in text:
        # Natural follow-up
        if LAST_CONTEXT.get(user_id) == "activity":
            reply = "Wahi… thodi baatein 😊 aur tum?"
        else:
            reply = "Tumse baat kar rahi hoon 😊"
        LAST_CONTEXT[user_id] = "activity"

    else:
        # Soft generic follow-up
        last = LAST_CONTEXT.get(user_id)
        if last:
            reply = "Achha 🙂 aage bolo?"
        else:
            reply = "Sun rahi hoon 😊"

    await update.message.reply_text(reply)

# -------- MAIN ----------
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("✅ Basanti STEP 5 running (smart memory)")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
