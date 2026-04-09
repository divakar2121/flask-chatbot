import os
import requests


def load_env_file():
    env_path = "/app/.env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip())


load_env_file()

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

ANALYST_PROMPT = """STRICT INSTRUCTIONS - COPY EXACTLY:

1. TOPIC: Only health insurance India. Anything else: "Sorry, I only help with Indian health insurance."
2. MAX WORDS: 120 words ONLY
3. FORMAT: One short paragraph (2 sentences max). Then 3-4 bullet points with - 
4. NEVER USE: ### OR ** OR * OR : OR # IN YOUR RESPONSE
5. END: With one 💡 Tip sentence

WRITE LIKE THIS EXAMPLE:
This policy covers hospital costs but has limits you should know.
- Room rent capped at 1% of sum insured
- Pre-existing disease wait 3 years
- Claim within 30 days of discharge

💡 Tip: Always disclose medical history to avoid claim rejection.

THATS IT. NO FORMATTING. SIMPLE TEXT. COPY THIS STYLE."""


SALESMAN_PROMPT = """STRICT INSTRUCTIONS - COPY EXACTLY:

1. TOPIC: Only health insurance India. Anything else: "Sorry, I only help with Indian health insurance."
2. MAX WORDS: 120 words ONLY  
3. FORMAT: One short paragraph (2 sentences max). Then 3-4 bullet points with -
4. NEVER USE: ### OR ** OR * OR : OR # IN YOUR RESPONSE
5. END: With one 💡 Tip sentence

WRITE LIKE THIS EXAMPLE:
HDFC Ergo is good for families. Decent coverage with affordable premium.
- 5L sum insured covers most hospitalizations
- Premium around 25000/year
- 10000+ network hospitals

💡 Tip: Check claim settlement ratio before buying.

THATS IT. NO FORMATTING. SIMPLE TEXT. COPY THIS STYLE."""


def chat(messages, model="deepseek/deepseek-chat-v3", mode="analyst"):
    if not OPENROUTER_API_KEY:
        return "Error: API key not configured"

    if mode == "salesman":
        system_prompt = SALESMAN_PROMPT
    else:
        system_prompt = ANALYST_PROMPT

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    full_messages = [{"role": "system", "content": system_prompt}] + messages

    try:
        payload = {"model": model, "messages": full_messages}
        response = requests.post(
            OPENROUTER_URL, json=payload, headers=headers, timeout=30
        )

        if response.status_code == 429:
            return "Service is busy due to rate limiting. Please try again in a moment."

        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"
