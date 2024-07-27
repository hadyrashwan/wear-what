create or replace function match_quote_embeddings (
  query_embedding vector(1024),
  match_threshold float,
  match_count int
)
returns table (
  id bigint,
  content text,
  similarity float
)
language sql stable
as $$
  select 
    quote_embeddings.id,
    quote_embeddings.quote_text,
    1 - (quote_embeddings.embedding <=> query_embedding) as similarity
  from quote_embeddings
  where 1 - (quote_embeddings.embedding <=> query_embedding) > match_threshold
  order by (quote_embeddings.embedding <=> query_embedding) asc
  limit match_count;
$$;