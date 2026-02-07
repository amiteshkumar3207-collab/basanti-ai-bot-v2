import requests
import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def ask_ai(user_text):
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://railway.app",
            "X-Title": "Basanti-AI-Bot"
        }

        payload = {
            "model": "qwen/qwen3-next-80b-a3b-instruct:free",
            "messages": [
                {"role": "system", "content": "You are Basanti, a friendly Hindi-English AI assistant."},
                {"role": "user", "content": user_text}
            ]
        }

        res = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=20
        )

        data = res.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print("AI ERROR:", e)
        return "⚠️ Thoda issue aaya hai, dobara try karo."
