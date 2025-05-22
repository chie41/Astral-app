# service/chatbot/ollama_client.py

import requests
import json
import sys
import time

class OllamaClient:
    def __init__(self, model="mistral", url="http://localhost:11434/api/generate"):
        self.model = model
        self.url = url

    def analyze_message(self, prompt: str) -> str:
        headers = {"Content-Type": "application/json"}
        data = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": 500,
            "stream": True
        }

        response = requests.post(self.url, json=data, headers=headers, stream=True)
        if response.status_code != 200:
            raise Exception(f"Ollama API error: {response.status_code} {response.text}")

        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line.decode("utf-8"))
                    text = chunk.get("response", "")
                    print(text, end="", flush=True)
                    full_response += text
                    time.sleep(0.01)
                except json.JSONDecodeError as e:
                    print(f"[Decode Error] {e}", file=sys.stderr)
        print()
        return full_response
