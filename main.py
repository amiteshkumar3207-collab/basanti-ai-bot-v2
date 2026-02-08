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

# -------- In-memory state ----------
LAST_MESSAGE = {}
LAST_CONTEXT = {}

# -------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Namaste 🙂\nMain Basanti hoon 🌸"
    )

# -------- WELCOME NEW MEMBERS ----------
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        name = member.first_name
        await update.message.reply_text(
            f"Swagat hai {name} 😊🌸\nMain Basanti hoon."
        )

# -------- CHAT ----------
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_type = update.effective_chat.type
    text = update.message.text.strip().lower()

    # -------- GROUP RULE ----------
    if chat_type in ["group", "supergroup"]:
        bot_username = context.bot.username.lower()
        if f"@{bot_username}" not in text:
            return  # ignore group messages without mention

        # remove mention
        text = text.replace(f"@{bot_username}", "").strip()

    # -------- REPEAT CHECK ----------
    if LAST_MESSAGE.get(user_id) == text:
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action="typing"
        )
        await asyncio.sleep(0.6)
        await update.message.reply_text("Haan, wahi 🙂 aage bolo?")
        return

    LAST_MESSAGE[user_id] = text

    # -------- TYPING ----------
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )
    await asyncio.sleep(0.8)

    # -------- INTENT ----------
    if any(x in text for x in ["hi", "hello", "hii"]):
        reply = "Hii 😊"
        LAST_CONTEXT[user_id] = "greeting"

    elif "naam" in text or "name" in text:
        reply = "Basanti 😄"
        LAST_CONTEXT[user_id] = "name"

    elif "kaisi ho" in text or "kaise ho" in text:
        reply = "Main theek hoon 🌸 tum?"
        LAST_CONTEXT[user_id] = "feeling"

    elif "kya kar" in text:
        reply = "Tumse baat kar rahi hoon 😊"
        LAST_CONTEXT[user_id] = "activity"

    else:
        reply = "Sun rahi hoon 😊"

    await update.message.reply_text(reply)

# -------- MAIN ----------
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("✅ Basanti STEP 6 running (group features)")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
