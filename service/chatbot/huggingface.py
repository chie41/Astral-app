print("Đang load huggingface.py")
import os
import re
import json
import requests
from dotenv import load_dotenv
from typing import Dict, Optional

load_dotenv()

class HuggingFaceClient:
    API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
    
    def __init__(self):
        self.headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

    def analyze_message(self, prompt: str) -> str:
        """Gửi prompt đến HuggingFace API và trả về response"""
        try:
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.7
                }
            }
            response = requests.post(
                self.API_URL,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json()[0]["generated_text"]
        except Exception as e:
            return f"❌ Lỗi API: {str(e)}"

    def extract_json(self, text: str) -> Optional[Dict]:
        """Trích xuất JSON từ response (nếu có)"""
        try:
            # Tìm JSON trong block ```json ```
            match = re.search(r"```json\s*({.*?})\s*```", text, re.DOTALL)
            if match:
                return json.loads(match.group(1))
            return None
        except json.JSONDecodeError:
            return None

# Ví dụ sử dụng
if __name__ == "__main__":
    client = HuggingFaceClient()
    response = client.analyze_message("Xin chào, bạn là gì?")
    print(response)