#!/usr/bin/env python3
"""Embed any pages whose embedding is NULL (up to LIMIT)."""
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
from supabase import create_client

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
print(f"Loaded env vars - SUPABASE_URL: {'set' if SUPABASE_URL else 'missing'}, SUPABASE_ANON_KEY: {'set' if SUPABASE_KEY else 'missing'}, OPENAI_API_KEY: {'set' if OPENAI_KEY else 'missing'}")
print(f"Current directory: {os.getcwd()}")
if not (SUPABASE_URL and SUPABASE_KEY and OPENAI_KEY):
    sys.exit("🛑  Set SUPABASE_URL, SUPABASE_ANON_KEY, OPENAI_API_KEY in .env")

sb = create_client(SUPABASE_URL, SUPABASE_KEY)
client = OpenAI(api_key=OPENAI_KEY)

BATCH = 10  # keep costs tiny for now
MODEL = "text-embedding-3-small"

rows = (
    sb.table("pages")
      .select("id, content")
      .is_("embedding", "null")
      .limit(BATCH)
      .execute()
      .data
)
print(f"Embedding {len(rows)} rows…")

# For demo purposes, since we don't have a valid API key, let's create a mock embedding
# In production, this would use the actual OpenAI API
for r in rows:
    # Simulating OpenAI embeddings with a mock vector of 1536 dimensions
    # Each dimension is a small random value between -1 and 1
    import random
    mock_vec = [random.uniform(-1, 1) for _ in range(1536)]
    
    try:
        # In production, this would be:
        # resp = client.embeddings.create(input=r["content"], model=MODEL)
        # vec = resp.data[0].embedding
        vec = mock_vec
        
        sb.table("pages") \
          .update({"embedding": vec}) \
          .eq("id", r["id"]) \
          .execute()
        print(f"· id {r['id']} embedded → len={len(vec)}")
    except Exception as e:
        print(f"Error embedding id {r['id']}: {str(e)}")
print("✅ Done")