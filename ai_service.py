import requests
from app.config.settings import settings

def ask_ai(prompt: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://railway.app",
        "X-Title": "Free Telegram AI Bot"
    }

    payload = {
        "model": settings.MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant. "
                    "Reply in simple Hindi or English. "
                    "Explain step by step."
                )
            },
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
