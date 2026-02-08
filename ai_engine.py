import os
import requests
from system_prompt import SYSTEM_PROMPT

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def ask_ai(user_messages):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://railway.app",
        "X-Title": "Basanti AI Bot"
    }

    payload = {
        "model": "openrouter/auto",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            *user_messages
        ],
        "temperature": 0.6
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
