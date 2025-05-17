from pydantic import BaseModel, Field
from typing import Optional, Union

class AskRequest(BaseModel):
    page_id: int = Field(1, gt=0)          # default to shard 1 for now
    question: str = Field(..., min_length=1, max_length=512)
    k: Optional[int] = Field(3, gt=0, le=5)  # how many shards to fetch

class AskResponse(BaseModel):
    answer: str
    metadata: dict = {
        "model": "gpt-4",
        "context_pages": [],
        "tokens_used": 0,
        "response_time_ms": 0,
        "error": None
    }

class VaultSaveRequest(BaseModel):
    page_id: int
    question: str
    answer: str