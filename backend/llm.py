import os
from pathlib import Path
from dotenv import load_dotenv
import requests
from backend.utils import format_items_for_prompt

# Load .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("API_KEY")

API_URL = "https://openrouter.ai/api/v1/chat/completions"

PROMPT_TEMPLATE = (
    "Based on the user's preference: \"{query}\" and the following {domain} items:\n\n"
    "{items}\n\n"
    "Generate 3 high-quality, personalized, and free recommendations with context and links."
)

def generate_response(query, items, domain):
    items_str = format_items_for_prompt(items)
    prompt = PROMPT_TEMPLATE.format(query=query, items=items_str, domain=domain)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "Recommendation System"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful recommendation system."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]

    except requests.exceptions.HTTPError as e:
        print("❌ HTTP ERROR:", e)
        print("🔍 Status code:", response.status_code)
        print("🔍 Response text:", response.text)
        return "😕 Oops, something went wrong. Invalid request or model."
    
    except Exception as e:
        print("❌ ERROR:", str(e))
        return "😕 Oops, something went wrong while fetching recommendations."
