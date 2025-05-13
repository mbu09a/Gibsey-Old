# Week 2 — Day 10 (Real RAG in `/ask`)

> **Target session:** ≈ 3 h  **Goal:** replace the stub answer with a true Retrieval‑Augmented Generation pipeline that pulls similar shards and calls GPT‑4o. Add latency & token‑cost headers for observability.
>
> **Outcome:** `/ask` responds with context‑aware answers; response headers expose timing & cost; round‑trip ≤ 1.5 s on average.

---

## 1 · Backend changes

### 1.1 Update `app/schemas.py`

```python
from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    page_id: int = Field(1, gt=0)
    question: str = Field(..., min_length=1, max_length=512)
    k: int | None = Field(3, gt=0, le=5)  # how many shards to fetch
```

### 1.2 Revise `/ask` route in `app/main.py`

```python
from fastapi import Response
from app.vector import similar_pages
from openai import OpenAI, APIError
import time, textwrap, os

OA_MODEL = "gpt-4o"
PRICE_PROMPT = 0.01 / 1000  # USD per 1k tokens (example)
PRICE_COMP  = 0.03 / 1000
client = OpenAI()

@app.post("/ask")
async def ask(req: AskRequest, res: Response):
    t0 = time.perf_counter()

    # 1 · fetch similar shards
    hits = await similar_pages(req.question, k=req.k)
    context = "\n---\n".join(textwrap.shorten(h["content"], 200) for h in hits)

    # 2 · build prompt
    system_msg = (
        "You are the narrator of a metafictional novel called Gibsey. "
        "Answer in ≤120 words, remain poetic but precise.\n\n"
        f"Context:\n{context}\n\nQuestion: {req.question}"
    )

    # 3 · call GPT‑4o
    try:
        resp = client.chat.completions.create(
            model=OA_MODEL,
            messages=[{"role": "user", "content": system_msg}],
            temperature=0.7,
            max_tokens=160,
        )
        answer = resp.choices[0].message.content.strip()
        usage  = resp.usage  # prompt_tokens, completion_tokens, total_tokens
    except APIError as e:
        res.status_code = 503
        return {"answer": "Gibsey is momentarily lost in the dream fog. Try again shortly."}

    # 4 · add observability headers
    latency_ms = round((time.perf_counter() - t0) * 1000)
    cost = round((usage.prompt_tokens * PRICE_PROMPT + usage.completion_tokens * PRICE_COMP), 4)
    res.headers.update({
        "X-Latency-MS": str(latency_ms),
        "X-Prompt-Tokens": str(usage.prompt_tokens),
        "X-Completion-Tokens": str(usage.completion_tokens),
        "X-Cost-USD": str(cost),
    })

    return {"answer": answer}
```

*(Adjust `PRICE_…` values to current OpenAI pricing.)*

### 1.3 Re‑build backend image

```bash
docker compose -f infra/compose.yaml build backend && docker compose up -d backend
```

---

## 2 · Frontend tweaks (`VaultTimeline` already in place)

Nothing required yet—answers are already displayed. If you want to surface headers for dev:

```ts
// in api.ts ask()
const r = await fetch(...);
console.log("latency", r.headers.get("X-Latency-MS"), "ms", "cost", r.headers.get("X-Cost-USD"));
```

---

## 3 · Local smoke test

```bash
curl -i -X POST http://localhost:8000/ask \
  -H 'Content-Type: application/json' \
  -d '{"page_id":1,"question":"Who is the mysterious Author?"}' | jq .
```

Check response headers for `X-Latency-MS` < 1500 and `answer` text contains a coherent reply.

---

## 4 · Logging (optional but quick)

Add at bottom of route:

```python
import json, pathlib, datetime as dt
log_dir = pathlib.Path("logs"); log_dir.mkdir(exist_ok=True)
log_dir.joinpath(f"ask-{dt.date.today()}.jsonl").write_text(
    json.dumps({"q": req.question, "t_ms": latency_ms, "tok": usage.total_tokens, "usd": cost})+"\n",
    append=True,
)
```

---

## 5 · Unit test (simple happy‑path)

`tests/test_ask.py` (skip in CI because of OpenAI call):

```python
import os, pytest, requests
pytestmark = pytest.mark.skipif(os.getenv("CI"), reason="LLM call")

def test_ask_live():
    r = requests.post("http://localhost:8000/ask", json={"page_id":1, "question":"test?"})
    assert r.status_code == 200 and "answer" in r.json()
```

---

## 6 · Commit & PR

```bash
git checkout -b day10-real-rag
git add apps/backend/app/main.py tests/test_ask.py
git commit -m "feat: real RAG in /ask with GPT-4o and metrics headers"
git push -u origin day10-real-rag
```

Open PR → **Closes #Day‑10 issue** → merge after green lint.
Move project card to **Done**.

---

### ✅ End‑of‑Day 10 Definition

* `/ask` uses similarity search + GPT‑4o, returns coherent answer.
* Headers `X-Latency-MS`, token counts, and cost present.
* Average latency observed < 1.5 s (console & curl confirm).

*Tomorrow (Day 11):* expose Vault timeline list in UI and swap Tailwind to full install.
