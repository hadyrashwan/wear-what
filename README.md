---
title: AI Weather and Clothing Suggestion App
emoji: 🌦️👚
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.24.0
app_file: app.py
pinned: true
license: mit
inference_file: weather_clothing_suggestion.py
base_model: mistralai/Mistral-7B-Instruct-v0.1
inference: true
---
# AI Weather and Clothing Suggestion App

This repository contains both a Streamlit app and a Hugging Face inference endpoint for providing weather information and AI-generated clothing suggestions based on current weather conditions.

## Streamlit App

The Streamlit app allows users to:
- Enter a city name to get current weather information
- Receive AI-generated clothing suggestions based on the weather
- View an AI-generated outfit visualization
- See a weather-related quote of the day

### Usage

To run the Streamlit app locally:

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Set up the necessary environment variables (API keys, etc.)
3. Run the app:
   ```
   streamlit run app.py
   ```

## Weather-based Clothing Suggestion Model

This model provides clothing suggestions based on given weather conditions. It uses the Mistral-7B-Instruct model to generate appropriate clothing recommendations.

### API Usage

To use this model via the Hugging Face Inference API, send a POST request with weather data in the following format:

```json
{
  "weather_data": {
    "temperature": 20,
    "weather": "Sunny",
    "description": "clear sky",
    "humidity": 60,
    "wind_speed": 5
  }
}
```

The model will return a clothing suggestion based on the provided weather conditions.

### Example

Input:
```json
{
  "weather_data": {
    "temperature": 20,
    "weather": "Sunny",
    "description": "clear sky",
    "humidity": 60,
    "wind_speed": 5
  }
}
```

Output:
```json
{
  "clothing_suggestion": "For a sunny day with a temperature of 20°C, clear skies, 60% humidity, and a light breeze of 5 m/s, I would suggest the following outfit:\n\nTop: A light, breathable short-sleeved t-shirt or a casual button-up shirt in a light color to reflect the sun.\n\nBottom: Comfortable khaki shorts or a light pair of jeans, depending on your preference and activities planned for the day.\n\nDon't forget to bring a light jacket or sweater in case the temperature drops later in the day, especially if you plan to be out in the evening."
}
```

## Repository Structure

- `app.py`: The main Streamlit application file
- `weather_clothing_suggestion.py`: The inference script for the clothing suggestion model
- `requirements.txt`: List of Python dependencies
- Other necessary files and assets

## Setup and Deployment

1. Ensure all files are in the root of your Hugging Face repository.
2. Set up the necessary secrets and environment variables in your Hugging Face space settings.
3. The Space will automatically deploy the Streamlit app based on the `app_file` specified in the YAML header.
4. The model inference will use the script specified by `inference_file` in the YAML header.

For any issues or suggestions, please open an issue in this repository.