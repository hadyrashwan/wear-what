import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from supabase import create_client, Client
from postgrest.exceptions import APIError

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Initialize SentenceTransformer
model = SentenceTransformer('thenlper/gte-small')

def process_text_file(file_path: str):
    # Read the file
    with open(file_path, 'r') as file:
        text = file.read()

    # Split the text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""],
        keep_separator=False,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)

    # Process each chunk
    for i, chunk in enumerate(chunks):
        # Further split the chunk into individual quotes
        quotes = chunk.split('\n')
        for j, quote in enumerate(quotes):
            # Skip empty lines
            if not quote.strip():
                continue

            # Create embedding
            embedding = model.encode(quote).tolist()

            # Extract quote number and text
            parts = quote.split('. ', 1)
            quote_number = parts[0] if len(parts) > 1 and parts[0].isdigit() else None
            quote_text = parts[1] if len(parts) > 1 else quote

            # Upload to Supabase
            supabase.table("quote_embeddings").insert({
                "chunk_id": f"{i}_{j}",
                "quote_number": quote_number,
                "quote_text": quote_text,
                "embedding": embedding
            }).execute()

    print(f"Processed and uploaded quotes to Supabase.")

# Usage
if __name__ == "__main__":
    file_path = "50_weather_quotes.txt"
    process_text_file(file_path)