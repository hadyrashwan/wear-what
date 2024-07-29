import { createClient } from "https://esm.sh/@supabase/supabase-js@2.39.7";

// Run local command
// deno run --unstable-cron --allow-env --allow-net  deno.ts
// make sure to set the envs in .env

// Get API keys from environment variables
const WEATHER_API_KEY = Deno.env.get("OPENWEATHERMAP_API_KEY");
const HF_API_KEY = Deno.env.get("HUGGINGFACE_API_KEY");
const SUPABASE_URL = Deno.env.get("SUPABASE_URL");
const SUPABASE_KEY = Deno.env.get("SUPABASE_KEY");



// Initialize Supabase
const supabase = createClient(SUPABASE_URL!, SUPABASE_KEY!);


async function fetchFirstRowFromSupabase() {
    const { data, error } = await supabase
      .from('quote_embeddings')  // Replace with your actual table name
      .select('*')
      .limit(1)
      .single();
  
    if (error) {
      console.error("Error fetching from Supabase:", error);
      return null;
    }
  
    return data;
  }
  
  // Deno cron job
Deno.cron("Supabase fetch", "0 0 * * *", async () => {
    console.log("Running daily Supabase fetch...");
    const row = await fetchFirstRowFromSupabase();
    if (row) {
      console.log("Fetched row:", row);
      // You can add more logic here to process the fetched row
    } else {
      console.log("No row fetched or an error occurred.");
    }
  })

async function callLlvmModel(prompt: string): Promise<string> {
  const llvmModelUrl = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3/v1/chat/completions";
  const payload = {
    model: "mistralai/Mistral-7B-Instruct-v0.3",
    messages: [
      {
        role: "user",
        content: prompt,
      }
    ],
    max_tokens: 500,
    stream: false
  };
  const headers = {
    "Authorization": `Bearer ${HF_API_KEY}`,
    "content-type": "application/json"
  };

  const response = await fetch(llvmModelUrl, {
    method: "POST",
    headers: headers,
    body: JSON.stringify(payload)
  });

  const data = await response.json();
  return data.choices[0].message.content;
}

async function generateOutfitImage(clothingSuggestion: string): Promise<Uint8Array> {
  const prompt = `A fashion illustration showing an outfit with ${clothingSuggestion}. Stylized, colorful, no text.`;
  
  const payload = {
    inputs: prompt,
    negative_prompt: "blurry, low quality, text, words, labels"
  };

  const API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1";
  const headers = { "Authorization": `Bearer ${HF_API_KEY}` };

  const response = await fetch(API_URL, {
    method: "POST",
    headers: headers,
    body: JSON.stringify(payload)
  });

  return new Uint8Array(await response.arrayBuffer());
}

async function getWeather(city: string): Promise<any> {
  const baseUrl = "http://api.openweathermap.org/data/2.5/weather";
  const url = new URL(baseUrl);
  url.searchParams.append("q", city);
  url.searchParams.append("appid", WEATHER_API_KEY!);
  url.searchParams.append("units", "metric");

  const response = await fetch(url.toString());
  return await response.json();
}

async function getAiClothingSuggestion(weatherData: any): Promise<string> {
  const prompt = `
    Given the following weather conditions:
    Temperature: ${weatherData.main.temp}°C
    Weather: ${weatherData.weather[0].main} (${weatherData.weather[0].description})
    Humidity: ${weatherData.main.humidity}%
    Wind Speed: ${weatherData.wind.speed} m/s

    Suggest appropriate clothing to wear, including top, bottom.
    Make sure to stick to hugging faces free response size limit.
  `;

  return await callLlvmModel(prompt);
}

async function getAiWeatherExplanation(weatherData: any): Promise<string> {
  const prompt = `
    Given the following weather conditions:
    Temperature: ${weatherData.main.temp}°C
    Weather: ${weatherData.weather[0].main} (${weatherData.weather[0].description})
    Humidity: ${weatherData.main.humidity}%
    Wind Speed: ${weatherData.wind.speed} m/s

    Give me the description of the weather.
    Make sure to stick to hugging faces free response size limit.
  `;

  return await callLlvmModel(prompt);
}

async function getRelevantQuote(weatherCondition: string): Promise<string> {
  const url = "https://api-inference.huggingface.co/models/mixedbread-ai/mxbai-embed-large-v1";

  const payload = { inputs: weatherCondition };
  const headers = {
    "content-type": "application/json",
    "Authorization": `Bearer ${HF_API_KEY}`
  };

  const response = await fetch(url, {
    method: "POST",
    headers: headers,
    body: JSON.stringify(payload)
  });

  const weatherEmbedding = await response.json();

  const { data, error } = await supabase.rpc("match_quote_embeddings", {
    query_embedding: weatherEmbedding,
    match_threshold: 0.5,
    match_count: 5
  });

  if (error) {
    console.error("Error fetching quote:", error);
    return "No relevant quote found.";
  }

  if (data && data.length > 0) {
    return data[0].content;
  } else {
    return "No relevant quote found.";
  }
}

// Example usage in a Deno Deploy function
Deno.serve(async (req) => {
  const url = new URL(req.url);
  const city = url.searchParams.get("city");

  if (!city) {
    return new Response("Please provide a city parameter", { status: 400 });
  }

  try {
    const weatherData = await getWeather(city);
    const clothingSuggestion = await getAiClothingSuggestion(weatherData);
    const weatherExplanation = await getAiWeatherExplanation(weatherData);
    const relevantQuote = await getRelevantQuote(weatherData.weather[0].main);

    const response = {
      weather: weatherData,
      clothingSuggestion,
      weatherExplanation,
      relevantQuote,
    };

    return new Response(JSON.stringify(response), {
      headers: { "Content-Type": "application/json" },
    });
  } catch (error) {
    console.error("Error:", error);
    return new Response("An error occurred", { status: 500 });
  }
});