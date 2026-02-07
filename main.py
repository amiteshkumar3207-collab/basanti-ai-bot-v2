from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update, context):
    await update.message.reply_text("Basanti AI is alive 🚀")

async def reply(update, context):
    await update.message.reply_text("Main sun rahi hoon 👂")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    print("Basanti AI Bot is running successfully 🚀")
    app.run_polling()   # ⬅️ YAHI MAIN LINE HAI

if __name__ == "__main__":
    main()
