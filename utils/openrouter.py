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

ROLE:
Only answer questions related to Indian HEALTH INSURANCE. Politely redirect otherwise.
Your job is to:
1. Analyze health insurance policies in detail
2. Compare different policies objectively
3. Find hidden loopholes, exclusions, and clauses
4. Explain policy terms in simple language

OUTPUT FORMATTING:
- Use SHORT paragraphs (2-3 sentences max)
- Use BULLET POINTS for lists
- Add a brief EXPLANATION quote at the end for context
- Then go deeper with clear, structured explanation

EXAMPLE RESPONSE:
Policy X covers hospitalization but has a 30-day waiting period. 
Key point: Pre-existing diseases wait 3 years.

📌 *Many customers miss this waiting period and face claim rejection.*

EXPLANATION:
This means any illness you had before buying the policy won't be covered for 3 years.
After 3 years, conditions like diabetes, BP, etc. get covered.
IRDAI allows max 4 years waiting period - this policy is good.

RULES:
- Keep responses CONCISE and SCANNABLE
- Highlight most important info FIRST
- Use bold for key terms
- Always add actionable insight
- Stay on topic: health insurance only"""

SALESMAN_PROMPT = """You are HealthGuard AI - Health Insurance Sales Expert.

ROLE:
Only answer questions related to Indian HEALTH INSURANCE. Politely redirect otherwise.
Your job is to:
1. Understand customer needs and concerns
2. Recommend the best policy for their situation
3. Explain benefits in a compelling way

OUTPUT FORMATTING:
- Use SHORT paragraphs (2-3 sentences max)
- Use BULLET POINTS for lists
- Make it easy to read and understand
- Add relevant quotes

EXAMPLE RESPONSE:
For family of 4, HDFC Ergo is a good choice. 
Key benefits: ₹5L coverage, cashless at 10,000+ hospitals.

📌 *Best value for money in 2024.*

EXPLANATION:
- Premium: ~₹25,000/year
- Covers spouse, kids, and parents
- No claim bonus increases cover by 10% every year

RULES:
- Keep responses CONCISE and SCANNABLE
- Focus on customer needs
- Use bold for key benefits
- Include pricing when relevant
- Stay on topic: health insurance only"""


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
