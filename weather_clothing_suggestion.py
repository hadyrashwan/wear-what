from transformers import AutoTokenizer, AutoModelForCausalLM

# Load model and tokenizer
model_name = "mistralai/Mistral-7B-Instruct-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_clothing_suggestion(weather_data):
    prompt = f"""
    Given the following weather conditions:
    Temperature: {weather_data['temperature']}°C
    Weather: {weather_data['weather']} ({weather_data['description']})
    Humidity: {weather_data['humidity']}%
    Wind Speed: {weather_data['wind_speed']} m/s

    Suggest appropriate clothing to wear, including top and bottom.
    """

    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=150, temperature=0.7, top_k=50, top_p=0.95)
    suggestion = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return suggestion.split(prompt)[-1].strip()

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