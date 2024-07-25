import streamlit as st
import requests
import datetime
import os
from huggingface_hub import InferenceClient
from sentence_transformers import SentenceTransformer
from supabase import create_client, Client
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Get API keys from environment variables
WEATHER_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY",)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY =  os.getenv("SUPABASE_KEY")

# Initialize the Hugging Face Inference Client
client = InferenceClient(token=HF_API_KEY)

# Initialize Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

model = SentenceTransformer('thenlper/gte-small')

def generate_outfit_image(clothing_suggestion):
    prompt = f"A fashion illustration showing an outfit with {clothing_suggestion}. Stylized, colorful, no text."
    
    # Generate image using Stable Diffusion via Hugging Face
    image_bytes = client.text_to_image(
        prompt,
        model="stabilityai/stable-diffusion-2-1",
        negative_prompt="blurry, low quality, text, words, labels",
    )
    
#    # Convert bytes to PIL Image
#     image = Image.open(BytesIO(image_bytes))
    return image_bytes

def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"  # For Celsius
    }
    response = requests.get(base_url, params=params)
    return response.json()

def get_ai_clothing_suggestion(weather_data):
    prompt = f"""
    Given the following weather conditions:
    Temperature: {weather_data['main']['temp']}°C
    Weather: {weather_data['weather'][0]['main']} ({weather_data['weather'][0]['description']})
    Humidity: {weather_data['main']['humidity']}%
    Wind Speed: {weather_data['wind']['speed']} m/s

    Suggest appropriate clothing to wear, including top, bottom.
    Make sure to stick to hugging faces free response size limit.
    """

    # Using Mistral 7B Instruct model via Hugging Face
    response = client.text_generation(
        prompt,
        model="mistralai/Mistral-7B-Instruct-v0.1",
        # max_new_tokens=150,
        temperature=0.7,
        # top_k=50,
        # top_p=0.95,
    )

    return response

def get_ai_weather_explanation(weather_data):
    prompt = f"""
    Given the following weather conditions:
    Temperature: {weather_data['main']['temp']}°C
    Weather: {weather_data['weather'][0]['main']} ({weather_data['weather'][0]['description']})
    Humidity: {weather_data['main']['humidity']}%
    Wind Speed: {weather_data['wind']['speed']} m/s

    Give me the description of the weather.
    Make sure to stick to hugging faces free response size limit.
    """

    # Using Mistral 7B Instruct model via Hugging Face
    response = client.text_generation(
        prompt,
        model="mistralai/Mistral-7B-Instruct-v0.1",
        max_new_tokens=150,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
    )

    return response

def get_relevant_quote(weather_condition):
    # Encode the weather condition
    weather_embedding = model.encode(weather_condition).tolist()

    response =  supabase.rpc("match_quote_embeddings",{
            'query_embedding': weather_embedding,
            'match_threshold': 0.5,
            'match_count': 5
    }).execute()


    if response.data and len(response.data) > 0:
        return response.data[0]['content']
    else:
        return "No relevant quote found."

st.title("AI-Powered Weather and Clothing Suggestion App")

city = st.text_input("Enter a city name:", "London")

if st.button("Get Weather and Clothing Suggestion"):
    weather_data = get_weather(city)
    
    if weather_data["cod"] != "404":
        main_weather = weather_data["weather"][0]["main"]
        description = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]
        
        st.subheader(f"Weather in {city}:")
        st.write(f"Condition: {main_weather} ({description})")
        st.write(f"Temperature: {temperature:.1f}°C")
        st.write(f"Humidity: {humidity}%")
        st.write(f"Wind Speed: {wind_speed} m/s")
        
        with st.spinner("Generating clothing suggestion..."):
            clothing_suggestion = get_ai_clothing_suggestion(weather_data)
        st.subheader("What to Wear (AI Suggestion):")
        st.write(clothing_suggestion)
        with st.spinner("Finding a relevant quote..."):
            weather_description = get_ai_weather_explanation(weather_data)
            quote = get_relevant_quote(f"{weather_description}")

        st.subheader("Quote of the Day:")
        st.write(quote)
        st.subheader("Weather description:")
        st.write(weather_description)
    else:
        st.error("City not found. Please check the spelling and try again.")

    with st.spinner("Generating outfit image..."):
        outfit_image = generate_outfit_image(clothing_suggestion)
    st.subheader("Outfit Visualization:")
    st.image(outfit_image, caption="AI-generated outfit based on the suggestion")

# Display current date and time
st.sidebar.write(f"Current Date and Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")