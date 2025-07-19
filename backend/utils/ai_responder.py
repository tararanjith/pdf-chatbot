import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")

def generate_response(query, chunks, history=None):
    if not OPENROUTER_API_KEY or not OPENROUTER_MODEL:
        print("❌ Missing OpenRouter API Key or Model in environment.")
        return "Error: AI model is not configured properly."

    context = "\n\n".join(chunks)

    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use the provided context when answering."},
        {"role": "system", "content": f"Context:\n{context}"}
    ]

    if history:
        messages.extend(history)

    messages.append({"role": "user", "content": query})

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": OPENROUTER_MODEL,
        "messages": messages
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as http_err:
        print("HTTP error occurred:", http_err)
        print("Response:", response.text)
        return "Error: Failed to generate a response from the AI model."
    except Exception as err:
        print("An error occurred:", err)
        return "Error: Unexpected failure during response generation."
