
# ai_engine.py
import os
import requests

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openrouter/auto"

def ask_ai(prompt):
    if not OPENROUTER_API_KEY:
        return "AI thodi der ke liye available nahi hai 😔"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://railway.app",
        "X-Title": "Basanti Bot"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Tum ek pyari ladki ho, naam Basanti. Hindi/Hinglish me short aur friendly reply karti ho."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        res = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=20)
        res.raise_for_status()
        data = res.json()
        return data["choices"][0]["message"]["content"]
    except Exception:
        return "Samajhne me thoda issue aa gaya 😅 Thodi der baad try karo."
