import requests
from config import DEEPSEEK_API_KEY

def ask_deepseek(user_input):
    url = "https://api.deepseek.com/v1"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }
    response = requests.post(url, headers=headers, json=payload, timeout=15)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]