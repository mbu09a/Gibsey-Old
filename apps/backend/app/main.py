from fastapi import Depends, FastAPI, HTTPException, Query
from starlette.middleware.cors import CORSMiddleware
from .config import Settings, get_settings
from .db import Supabase
from .schemas import AskRequest, AskResponse
import time

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health(settings: Settings = Depends(get_settings)):
    return {"status": "ok", "env": settings.env}

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
    start = time.perf_counter()
    # 🚧  Placeholder answer — replace with real RAG later
    answer = (
        "[stub] I see you asked: '" + req.question.strip() + "'. "
        "Gibsey will reply in full once the Dream engine is online."
    )
    elapsed = (time.perf_counter() - start) * 1000
    print(f"/ask latency {elapsed:.0f} ms")
    return {"answer": answer}