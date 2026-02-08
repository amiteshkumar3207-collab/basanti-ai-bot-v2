from telegram.ext import Application, CommandHandler
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update, context):
    await update.message.reply_text("Hello 👋 Bot alive hai")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    print("Bot started")
    app.run_polling()
