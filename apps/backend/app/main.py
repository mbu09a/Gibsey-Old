from fastapi import Depends, FastAPI, HTTPException, Query, Response
from starlette.middleware.cors import CORSMiddleware
from openai import OpenAI, APIError
from .config import Settings, get_settings
from .db import Supabase
from .schemas import AskRequest, AskResponse, VaultSaveRequest
from .vector import similar_pages, get_openai_client
import time
import textwrap
import json
import pathlib
import datetime as dt

app = FastAPI(
    title="Gibsey Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Gibsey Backend API is running!",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi_schema": "/openapi.json"
    }
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_methods=["*"],
    allow_headers=["*"],
)

# Debug endpoint to list all routes
@app.get("/routes")
async def list_routes():
    routes = []
    for route in app.routes:
        if hasattr(route, "methods"):
            routes.append({
                "path": route.path,
                "methods": sorted(list(route.methods)),
                "name": getattr(route, "name", ""),
                "endpoint": getattr(route, "endpoint", "").__name__ if hasattr(route, "endpoint") else ""
            })
    return {"routes": routes}

@app.get("/health")
async def health(settings: Settings = Depends(get_settings)):
    return {"status": "ok", "env": settings.env}

@app.get("/debug")
async def debug():
    import os
    import inspect
    
    # Get the absolute path of the current file
    current_file = os.path.abspath(__file__)
    
    # Read the first 100 lines of the file
    file_content = []
    try:
        with open(current_file, 'r') as f:
            file_content = [f"{i+1}: {line.rstrip()}" for i, line in enumerate(f) if i < 100]
    except Exception as e:
        file_content = [f"Error reading file: {str(e)}"]
    
    return {
        "current_file": current_file,
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "file_exists": os.path.exists(current_file),
        "file_content": "\n".join(file_content)
    }

@app.get("/read")
async def read_page(id: int = Query(..., gt=0)):
    page = (
        Supabase.client()
        .table("pages")
        .select("id,title,content,symbol_id")
        .eq("id", id)
        .single()
        .execute()
        .data
    )
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page

# OpenAI pricing constants (adjust to current rates)
PRICE_PROMPT = 0.01 / 1000  # USD per 1k tokens for prompt
PRICE_COMP = 0.03 / 1000     # USD per 1k tokens for completion

@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest, response: Response):
    """Handle questions using RAG with GPT-4o and vector search."""
    t0 = time.perf_counter()
    
    try:
        # 1. Fetch similar shards using vector search
        hits = await similar_pages(req.question, k=req.k or 3)
        
        # Create context from top hits
        context = "\n---\n".join(
            f"Page {h['page_id']}: {textwrap.shorten(h.get('content', ''), 200, placeholder='...')}" 
            for h in hits
        )
        
        # 2. Build the prompt for GPT-4o
        system_msg = (
            "You are the narrator of a metafictional novel called Gibsey. "
            "Answer in ≤120 words, remain poetic but precise.\n\n"
            f"Context:\n{context}\n\nQuestion: {req.question}"
        )
        
        # 3. Call GPT-4o
        client = get_openai_client()
        try:
            resp = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": system_msg}],
                temperature=0.7,
                max_tokens=160,
            )
            answer = resp.choices[0].message.content.strip()
            usage = resp.usage  # prompt_tokens, completion_tokens, total_tokens
        except APIError as e:
            response.status_code = 503
            return {
                "answer": "Gibsey is momentarily lost in the dream fog. Try again shortly.",
                "metadata": {"error": str(e), "model": "gpt-4o"}
            }
        
        # 4. Calculate metrics
        latency_ms = round((time.perf_counter() - t0) * 1000)
        cost = round((usage.prompt_tokens * PRICE_PROMPT + usage.completion_tokens * PRICE_COMP), 4)
        
        # 5. Add observability headers
        response.headers.update({
            "X-Latency-MS": str(latency_ms),
            "X-Prompt-Tokens": str(usage.prompt_tokens),
            "X-Completion-Tokens": str(usage.completion_tokens),
            "X-Cost-USD": str(cost),
        })
        
        # 6. Log the interaction (optional)
        log_dir = pathlib.Path("logs")
        log_dir.mkdir(exist_ok=True)
        log_entry = {
            "timestamp": dt.datetime.utcnow().isoformat(),
            "question": req.question,
            "answer": answer,
            "latency_ms": latency_ms,
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "cost_usd": cost,
            "context_pages": [h["page_id"] for h in hits]
        }
        log_file = log_dir / f"ask-{dt.date.today()}.jsonl"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        # 7. Return the response
        return {
            "answer": answer,
            "metadata": {
                "model": "gpt-4o",
                "context_pages": [h["page_id"] for h in hits],
                "tokens_used": usage.total_tokens,
                "response_time_ms": latency_ms,
                "cost_usd": cost,
                "error": None
            }
        }
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error in /ask endpoint: {error_msg}")
        latency_ms = round((time.perf_counter() - t0) * 1000)
        response.status_code = 500
        
        # Log the error
        log_dir = pathlib.Path("logs")
        log_dir.mkdir(exist_ok=True)
        log_entry = {
            "timestamp": dt.datetime.utcnow().isoformat(),
            "question": req.question if 'req' in locals() else "Unknown",
            "error": error_msg,
            "latency_ms": latency_ms
        }
        log_file = log_dir / f"errors-{dt.date.today()}.jsonl"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        return {
            "answer": "I'm sorry, I encountered an error while processing your question. Please try again later.",
            "metadata": {
                "model": "gpt-4o",
                "context_pages": [],
                "tokens_used": 0,
                "response_time_ms": latency_ms,
                "error": error_msg
            }
        }

@app.post("/vault/save", status_code=201)
async def save_to_vault(req: VaultSaveRequest):
    Supabase.client() \
        .table("vault") \
        .insert({
            "page_id": req.page_id,
            "question": req.question,
            "answer": req.answer,
        }) \
        .execute()
    return {"ok": True}