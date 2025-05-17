from fastapi import Depends, FastAPI, HTTPException, Query
from starlette.middleware.cors import CORSMiddleware
from .config import Settings, get_settings
from .db import Supabase
from .schemas import AskRequest, AskResponse, VaultSaveRequest
import time

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

@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    print("DEBUG: UPDATED /ask endpoint called with question:", req.question)  # Debug print
    start = time.perf_counter()
    response_metadata = {
        "model": "gpt-4",
        "context_pages": [],
        "tokens_used": 0,
        "response_time_ms": 0,
        "error": None
    }
    
    # Temporary response to verify code updates - VERSION 2
    elapsed = (time.perf_counter() - start) * 1000
    return {
        "answer": "THIS IS A TEST RESPONSE - VERSION 2 - The RAG system is working correctly!",
        "metadata": {
            **response_metadata,
            "response_time_ms": round(elapsed, 2),
            "debug": "This is a test response to verify code updates"
        }
    }
    
    try:
        # Get relevant pages using vector search
        from .vector import similar_pages
        from .llm import generate_answer
        
        # Get the most relevant pages
        relevant_pages = similar_pages(req.question, k=3)
        response_metadata["context_pages"] = [
            {"id": p["id"], "title": p["title"], "score": p["score"]}
            for p in relevant_pages
        ]
        
        if not relevant_pages:
            response_metadata["error"] = "No relevant pages found"
            return {
                "answer": "I couldn't find any relevant information to answer your question.",
                "metadata": response_metadata
            }
        
        # Generate an answer using GPT-4
        answer = generate_answer(req.question, relevant_pages)
        
        # Calculate response time
        elapsed = (time.perf_counter() - start) * 1000
        response_metadata["response_time_ms"] = round(elapsed, 2)
        
        print(f"/ask processed in {elapsed:.0f} ms")
        
        return {
            "answer": answer,
            "metadata": response_metadata
        }
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error in /ask endpoint: {error_msg}")
        response_metadata["error"] = error_msg
        response_metadata["response_time_ms"] = round((time.perf_counter() - start) * 1000, 2)
        
        return {
            "answer": "I'm sorry, I encountered an error while processing your question. Please try again later.",
            "metadata": response_metadata
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