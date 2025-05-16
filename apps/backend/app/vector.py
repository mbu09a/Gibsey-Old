from typing import List, Dict
from supabase import Client
from .db import Supabase
from openai import OpenAI
import os
from .config import get_settings

MODEL = "text-embedding-3-small"
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY") or get_settings().openai_api_key)


def _embed(text: str) -> List[float]:
    """Return OpenAI embedding vector for the query string."""
    resp = client.embeddings.create(model=MODEL, input=text)
    return resp.data[0].embedding


def similar_pages(query: str, k: int = 3) -> List[Dict]:
    """Return top‑k pages ordered by cosine similarity.
    
    Args:
        query: The text to find similar pages for
        k: Number of results to return (default: 3)
        
    Returns:
        List of dicts with id, title, content and similarity score
    """
    vec = _embed(query)
    sb: Client = Supabase.client()
    rows = (
        sb.rpc(
            "match_pages",  # Postgres function for vector similarity
            {"query_embedding": vec, "match_k": k},
        )
        .execute()
        .data
    )
    return rows  # [{id, title, content, score}]