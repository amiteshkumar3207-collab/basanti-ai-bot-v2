import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

# ====== CONFIG ======
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "Tum Basanti ho – ek friendly, samajhdaar virtual dost. "
        "Natural Hindi/Hinglish me baat karo. "
        "Repeat mat karo. Short, human-like replies do. "
        "Khud ko AI ya bot bolne ki zarurat nahi."
    )
)

chat_sessions = {}

# ====== HANDLERS ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hii 😊 main Basanti hoon 🌼\n"
        "Aaj ka din kaisa ja raha hai?"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in chat_sessions:
        chat_sessions[user_id] = model.start_chat(history=[])

    response = chat_sessions[user_id].send_message(text)
    await update.message.reply_text(response.text)

# ====== MAIN ======
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("Basanti is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
