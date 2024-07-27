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
base_model: mistralai/Mistral-7B-Instruct-v0.3
pipeline_tag: text-generation
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

