import os
from telegram import Update, ChatPermissions
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = 1085953633  # tumhari Telegram user ID

# ---------- LADY AI LOGIC ----------
def ai_reply_logic(text: str):
    text = text.lower()

    if "hi" in text or "hello" in text:
        return "Hii 😊 main yahin hoon"
    if "kaise ho" in text:
        return "Main bilkul theek hoon 😊 aap kaise ho?"
    if "tum kaun ho" in text:
        return "Main ek lady AI Telegram bot hoon 👩‍💻"
    if "kya kar rahi ho" in text:
        return "Bas aap se baat kar rahi hoon 😊"
    if "name" in text or "naam" in text:
        return "Aap mujhe *Basanti* keh sakte ho 💕"
    if "help" in text:
        return "Aap /help likh kar commands dekh sakte ho 🙂"
    if "thank" in text or "thanks" in text:
        return "Welcome 😊 khushi hui madad karke"

    return "Achha 😊 thoda aur batao na"

# ---------- HELP ----------
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👩‍🦰 *Basanti Bot Commands*\n\n"
        "/help - Help message\n\n"
        "*Group Admin Only:*\n"
        "/rules - Group rules\n"
        "/boton - Bot ON\n"
        "/botoff - Bot OFF\n"
        "/mute (reply) - 5 min mute\n\n"
        "*Owner Only:*\n"
        "/broadcast <msg>\n"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

# ---------- CHECK GROUP ADMIN ----------
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
        return
    await update.message.reply_text("📜 Group Rules:\n1. Respect everyone\n2. No spam")

async def boton(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_group_admin(update, context):
        return
    context.chat_data["bot_enabled"] = True
    await update.message.reply_text("😊 Theek hai, bot ON kar diya")

async def botoff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_group_admin(update, context):
        return
    context.chat_data["bot_enabled"] = False
    await update.message.reply_text("🙈 Bot OFF kar diya")

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_group_admin(update, context):
        return
    if not update.message.reply_to_message:
        return await update.message.reply_text("Reply karke /mute likho 🙂")
    user_id = update.message.reply_to_message.from_user.id
    await context.bot.restrict_chat_member(
        chat_id=update.effective_chat.id,
        user_id=user_id,
        permissions=ChatPermissions(can_send_messages=False),
        until_date=300,
    )
    await update.message.reply_text("🤫 Thodi der ke liye mute kar diya")

# ---------- OWNER ----------
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    await update.message.reply_text("📢 Owner message delivered 😊")

# ---------- WELCOME ----------
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(
            f"👋 Welcome {member.first_name} 😊\nGroup rules follow karna"
        )

# ---------- AUTO REPLY ----------
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ["group", "supergroup"]:
        if context.chat_data.get("bot_enabled") is False:
            return
    reply = ai_reply_logic(update.message.text)
    await update.message.reply_text(reply)

# ---------- MAIN ----------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("rules", rules))
    app.add_handler(CommandHandler("boton", boton))
    app.add_handler(CommandHandler("botoff", botoff))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("broadcast", broadcast))

    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    app.run_polling()

if __name__ == "__main__":
    main()
