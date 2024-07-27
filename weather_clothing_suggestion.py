import requests
import os
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY",)

def call_llvm_model(prompt):
    llvm_model_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3/v1/chat/completions"
    payload = {
    "model": "mistralai/Mistral-7B-Instruct-v0.3",
    "messages": [
        {
        "role": "user",
        "content": prompt,
        }
    ],
    "max_tokens": 500,
    "stream": False
    }
    headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "content-type": "application/json"
    }

    response = requests.post(llvm_model_url, json=payload, headers=headers)

    response = response.json()
    return response['choices'][0]['message']['content']


def generate_clothing_suggestion(weather_data):
    prompt = f"""
    Given the following weather conditions:
    Temperature: {weather_data['temperature']}°C
    Weather: {weather_data['weather']} ({weather_data['description']})
    Humidity: {weather_data['humidity']}%
    Wind Speed: {weather_data['wind_speed']} m/s

    Suggest appropriate clothing to wear, including top and bottom.
    """

    return call_llvm_model(prompt)

def inference(weather_data):
    try:
        clothing_suggestion = generate_clothing_suggestion(weather_data)
        return {"clothing_suggestion": clothing_suggestion}
    except Exception as e:
        return {"error": str(e)}

# Hugging Face format for custom inference API
def run(data):
    weather_data = data.get("weather_data", {})
    if not weather_data:
        return {"error": "No weather data provided"}
    
    result = inference(weather_data)
    return result