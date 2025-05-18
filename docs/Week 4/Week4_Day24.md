# Week 4 — Day 24 (Dual‑Store Routing Helper)

> **Target session:** ≈ 3 h  **Goal:** teach the backend to decide—at runtime—whether to use **pgvector** or **Pinecone** for similarity search. Threshold: if total `pages` rows > 500, use Pinecone; else fall back to pgvector. Update `/ask` accordingly and add unit tests.
>
> **Outcome:** Queries against the full 743‑page corpus hit Pinecone and return answers in ≤ 1.2 s P90 latency.

---

\## 1 · Add Pinecone query helper
Extend **`app/vector.py`**

```python
from pinecone import Pinecone, ServerlessSpec

_PINE_ENV  = os.getenv("PINE_ENV")
_PINE_KEY  = os.getenv("PINE_API_KEY")
_PINE_NAME = os.getenv("PINE_INDEX")

pc: Pinecone | None = None
idx = None

def get_pc_index():
    global pc, idx
    if pc is None:
        pc = Pinecone(api_key=_PINE_KEY, environment=_PINE_ENV)
        idx = pc.Index(_PINE_NAME)
    return idx

async def pinecone_similar(query:str, k:int=3):
    emb = _oa.embeddings.create(model=_MODEL, input=query).data[0].embedding
    index = get_pc_index()
    res = index.query(vector=emb, top_k=k, include_metadata=True)
    return [
        {"id": int(m.id), "content": m.metadata["content"], "score": 1 - m.score}
        for m in res.matches
    ]
```

---

\## 2 · Corpus‑size check
Add cached count:

```python
from functools import lru_cache

@lru_cache(maxsize=1)
def corpus_size() -> int:
    return _sb.table("pages").select("id", count="exact").execute().count or 0
```

Modify exported `similar_pages`:

```python
async def similar_pages(text:str, k:int=3):
    if corpus_size() > 500 and _PINE_KEY:
        return await pinecone_similar(text, k)
    return await pgvector_similar(text, k)  # rename old function
```

---

\## 3 · Unit test with monkeypatch
`tests/test_dual.py`:

```python
import pytest, asyncio
from app.vector import similar_pages, pinecone_similar, pgvector_similar

@pytest.mark.asyncio
async def test_routing(monkeypatch):
    # force corpus_size to 1000
    monkeypatch.setattr("app.vector.corpus_size", lambda: 1000)
    monkeypatch.setattr("app.vector._PINE_KEY", "fake")
    called = {"pine":False,"pg":False}
    async def fake_pc(*a,**kw): called["pine"]=True; return []
    async def fake_pg(*a,**kw): called["pg"]=True; return []
    monkeypatch.setattr("app.vector.pinecone_similar", fake_pc)
    monkeypatch.setattr("app.vector.pgvector_similar", fake_pg)
    await similar_pages("test",3)
    assert called["pine"] and not called["pg"]
```

CI skip if no Pinecone key.

---

\## 4 · Update `/ask` latency header test
No API change—just ensure real query hits Pinecone (check backend logs).

---

\## 5 · Manual benchmark
Run `scripts/bench.py` (created Day 25 tomorrow) beforehand:

```bash
python scripts/bench.py --n 20 --pinecone
```

Ensure P90 latency < 1.2 s.

---

\## 6 · Commit & PR

```bash
git checkout -b day24-dual-routing
git add apps/backend/app/vector.py apps/backend/tests/test_dual.py
git commit -m "feat: dual‑store routing between pgvector and Pinecone"
git push -u origin day24-dual-routing
```

PR → **Closes #Day‑24 issue** → merge after CI green.
Move card to **Done**.

---

\### ✅ End‑of‑Day 24 Definition

* `similar_pages()` automatically chooses Pinecone when corpus > 500.
* Unit test proves routing branch.
* Manual query shows Pinecone calls & maintains latency target.

*Tomorrow (Day- 25):* build latency benchmark script and wire it into CI.