import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ===== ENV =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ===== GEMINI CONFIG =====
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "Tum Basanti ho. "
        "Tum friendly, samajhdaar aur simple Hindi/Hinglish me baat karti ho. "
        "Tum khud ko AI ya bot nahi bolti. "
        "Short, natural replies deti ho. "
        "Repeat reply nahi karti."
    )
)

chats = {}

# ===== START COMMAND =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hii 😊 main Basanti hoon 🌸\n"
        "Aaram se baat karo, main sun rahi hoon 🙂"
    )

# ===== CHAT HANDLER =====
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in chats:
        chats[user_id] = model.start_chat(history=[])

    try:
        response = chats[user_id].send_message(text)
        reply = response.text
    except Exception:
        reply = "Thoda sa issue aa gaya 😅 fir se likho na"

    await update.message.reply_text(reply)

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("Basanti bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
