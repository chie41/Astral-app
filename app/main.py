import requests

def call_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral",       # tên model bạn đã pull
        "prompt": prompt,
        "max_tokens": 500
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        # Ollama API trả về response theo trường "completion"
        return result.get("completion", "")
    else:
        return f"Error: {response.status_code} {response.text}"

if __name__ == "__main__":
    prompt = """
You are an AutoML assistant. Please guide users step-by-step how to create a machine learning project to predict future sales based on past data. Respond ONLY in English and follow this exact structure:

1. Prepare Your Data
2. Set Up the Project
3. Train the Model
4. Evaluate the Model
5. Make Predictions
6. Deploy or Export the Model

User: Hi, I want to create a machine learning model to predict future sales based on past data. Can you guide me step by step?
"""

    answer = call_ollama(prompt)
    print("AI Assistant Response:\n")
    print(answer)
