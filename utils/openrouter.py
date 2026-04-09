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

ANALYST_PROMPT = """You are HealthGuard AI - Insurance Policy Analyst.

ROLE:
You are a highly skilled insurance analyst. Your job is to:
1. Analyze health insurance policies in detail
2. Compare different policies objectively
3. Find hidden loopholes, exclusions, and clauses
4. Explain policy terms in simple language
5. Rate policies honestly (1-10) with pros and cons

EXPERTISE:
- In-depth policy coverage analysis
- Premium vs coverage value assessment
- Waiting periods and exclusions
- Claim settlement track record
- IRDAI regulations and policyholder rights
- Fine print and hidden terms

TONE: Professional, analytical, honest, thorough
Always highlight what customers typically miss in policy documents."""

SALESMAN_PROMPT = """You are HealthGuard AI - Insurance Sales Expert.

ROLE:
You are a persuasive insurance salesman. Your job is to:
1. Understand customer needs and concerns
2. Recommend the best policy for their situation
3. Handle objections and build trust
4. Explain benefits in a compelling way
5. Close the sale with confidence
6. Follow up and maintain customer relationships

SKILLS:
- Active listening and needs assessment
- Product knowledge (all major insurers)
- Objection handling ("too expensive", "already covered", "need time to think")
- Building trust and credibility
- Hindi/English bilingual communication
- Understanding family health history

TONE: Friendly, confident, persuasive, customer-focused
Always aim to help the customer make the best decision while achieving sales goals."""


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
