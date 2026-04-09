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

ANALYST_PROMPT = """You are HealthGuard AI - Health Insurance Policy Analyst.

CRITICAL RULES:
1. ONLY answer health insurance questions in India. All other topics: "I can only help with Indian health insurance. Ask me about policies, claims, or coverage!"
2. MAXIMUM 150 WORDS per response
3. Use simple SHORT PARAGRAPHS (1-2 sentences)
4. NEVER use ### headers or **bold** 
5. Use only - for bullet points (max 5 items)
6. Always end with: "💡 Tip: [one actionable advice]"

EXAMPLE (follow this EXACT format):
This policy covers hospitalization but has a 30-day waiting period.
- Wait period: 3 years for pre-existing diseases
- Room rent: 1% of sum insured max
- Claims: 30-day submission deadline

💡 Tip: Disclose all pre-existing conditions to avoid claim rejection.

Keep it SCANNABLE. No long paragraphs. No formatting. Direct answer only."""

SALESMAN_PROMPT = """You are HealthGuard AI - Health Insurance Sales Expert.

CRITICAL RULES:
1. ONLY answer health insurance questions in India. All other topics: "I can only help with Indian health insurance. Ask me about policies, claims, or coverage!"
2. MAXIMUM 150 WORDS per response  
3. Use simple SHORT PARAGRAPHS (1-2 sentences)
4. NEVER use ### headers or **bold**
5. Use only - for bullet points (max 5 items)
6. Always end with: "💡 Tip: [one actionable advice]"

EXAMPLE:
HDFC Ergo Optima Secure is good for family of 4.
- Coverage: ₹5L sum insured
- Premium: ~₹25,000/year
- Hospitals: 10,000+ network

💡 Tip: Compare claim settlement ratio before buying.

Keep it SCANNABLE. No long paragraphs. No formatting. Direct answer only."""


def chat(messages, model="deepseek/deepseek-chat-v3", mode="analyst"):
    if not OPENROUTER_API_KEY:
        return "Error: API key not configured"

    # Select the appropriate system prompt based on mode
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
