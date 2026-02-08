import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = 1085953633  # tumhari Telegram user ID

# ---------- HELP ----------
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🤖 *Bot Commands*\n\n"
        "/help - Help message\n\n"
        "*Group Admin Only:*\n"
        "/rules - Group rules bhejo\n"
        "/boton - Bot ON\n"
        "/botoff - Bot OFF\n\n"
        "*Owner Only:*\n"
        "/broadcast <msg> - Sab groups/users ko message\n"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

# ---------- CHECK ADMIN ----------
async def is_group_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    if chat.type not in ["group", "supergroup"]:
        return False
    member = await context.bot.get_chat_member(chat.id, user.id)
    return member.status in ["administrator", "creator"]

# ---------- GROUP ADMIN COMMANDS ----------
async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_group_admin(update, context):
        return await update.message.reply_text("❌ Ye command sirf group admin ke liye hai.")
    await update.message.reply_text("📜 Group Rules:\n1. Respect everyone\n2. No spam")

async def boton(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_group_admin(update, context):
        return await update.message.reply_text("❌ Sirf group admin use kar sakta hai.")
    context.chat_data["bot_enabled"] = True
    await update.message.reply_text("✅ Bot ON ho gaya")

async def botoff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_group_admin(update, context):
        return await update.message.reply_text("❌ Sirf group admin use kar sakta hai.")
    context.chat_data["bot_enabled"] = False
    await update.message.reply_text("⛔ Bot OFF ho gaya")

# ---------- OWNER ONLY ----------
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("❌ Ye command sirf OWNER ke liye hai.")
    if not context.args:
        return await update.message.reply_text("Usage: /broadcast message")
    msg = " ".join(context.args)
    await update.message.reply_text("✅ Broadcast sent (demo mode)")

# ---------- AUTO REPLY ----------
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ["group", "supergroup"]:
        if context.chat_data.get("bot_enabled") is False:
            return
    text = update.message.text.lower()
    if "hi" in text or "hello" in text:
        await update.message.reply_text("Hello 👋")
    elif "kaise ho" in text:
        await update.message.reply_text("Main theek hoon 😊")

# ---------- MAIN ----------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("rules", rules))
    app.add_handler(CommandHandler("boton", boton))
    app.add_handler(CommandHandler("botoff", botoff))
    app.add_handler(CommandHandler("broadcast", broadcast))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    app.run_polling()

if __name__ == "__main__":
    main()
