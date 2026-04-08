import os
import requests

OPENROUTER_API_KEY = os.environ.get(
    "OPENROUTER_API_KEY",
    "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",
)
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def chat(messages, model="openai/gpt-3.5-turbo"):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": os.environ.get("HTTP_REFERER", "https://your-app.render.app"),
        "X-Title": "Flask Chatbot",
    }

    payload = {"model": model, "messages": messages}

    response = requests.post(OPENROUTER_URL, json=payload, headers=headers, timeout=30)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]
