# Make sure to enable pg_vector extension
CREATE TABLE public.quote_embeddings (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    chunk_id TEXT,
    quote_number TEXT,
    quote_text TEXT,
    embedding VECTOR(1024)
);