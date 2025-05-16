-- match_pages(query_embedding float8[], match_k int)
create or replace function match_pages(query_embedding vector, match_k int = 3)
returns table (
  id        bigint,
  title     text,
  content   text,
  score     float
) language sql stable as $$
  select id, title, content,
         1 - (embedding <=> query_embedding) as score
  from pages
  order by embedding <=> query_embedding
  limit match_k;
$$;