# Week 7 — Day 47 (Symbol Filter Logic & Latency Validation)

> **Target session:** ≈ 3 h  **Goal:** wire the 16‑symbol palette into query flow so `/ask` can limit similarity search to a selected `symbol_id`. Update benchmark to measure latency with the filter enabled and keep P90 ≤ 2 s.
>
> **Outcome:** Choosing a symbol chip filters answers to shards with that symbol; timeline shows colored trail; benchmark script passes at ≤ 2 s even with filter.

---

## 1 · Backend — accept `symbol_id` in `/ask`

### 1.1 Update request model

```python
class AskRequest(BaseModel):
    page_id: int | None = None  # legacy
    question: str
    k: int = 50
    symbol_id: int | None = None   # NEW
```

### 1.2 Pass filter to `similar_pages`

```python
similar = await similar_pages(req.question, k=req.k, symbol_id=req.symbol_id)
```

### 1.3 Extend `similar_pages` helper

```python
aasync def pgvector_similar(text:str, k:int, symbol_id:int|None=None):
    emb = await embed(text)
    q = sb.table("pages").select("id,title,content,symbol_id", "score")\
        .order("embedding", query_vector=emb)\
        .limit(k)
    if symbol_id is not None:
        q = q.eq("symbol_id", symbol_id)
    return q.execute().data
```

For Pinecone query, filter metadata in `index.query`:

```python
filter={"symbol_id": symbol_id} if symbol_id is not None else None
res = index.query(vector=emb, top_k=k, filter=filter, include_metadata=True)
```

Ensure `symbol_id` already saved in metadata during Day 23 upserts.

---

## 2 · Front‑end — pass selected symbol

### 2.1 Extend symbol picker state

In parent component (reader/vault page):

```tsx
const [symbolFilter,setSymbolFilter]=useState<number|"all">("all");
```

SymbolBar `onPick` sets state; pass to Ask form:

```tsx
await apiFetch("/ask", {method:"POST", body:JSON.stringify({question, k:50, symbol_id: symbolFilter === "all"? null : symbolFilter})});
```

### 2.2 Color trail on answer cards

Add small colored left border:

```tsx
<div className={`border-l-4 pl-3 ${SYMBOL_COLORS[hit.symbol_id]}`}>...</div>
```

`SYMBOL_COLORS` maps id → `border-emerald-500`, etc.

---

## 3 · Update benchmark script

In `scripts/bench.py` add CLI flag:

```python
ap.add_argument('--symbol', type=int, default=None)
...
payload = {"question": q, "symbol_id": args.symbol}
```

Run two batches—unfiltered & filtered—and emit separate CSV rows.

---

## 4 · Latency test & adjustment

1. **Local benchmark:**

```bash
python scripts/bench.py --n 30 --symbol 5  # filter to symbol 5
```

Expect P90 ≤ 1.3 s.
2\. If latency > 1.8 s:

* Reduce `k` default to 30 for filtered queries.
* Upgrade Pinecone pod (one size up).
* Cache embeddings for identical questions per user.

---

## 5 · Axe / a11y regression

Ensure symbol chips still have `aria-label="Symbol 5"`; keyboard arrow scroll possible; no focus trap.

---

## 6 · Commit & PR

```bash
git checkout -b day47-symbol-filter
# backend changes, benchmark, frontend SymbolBar integration
git add apps/backend apps/frontend scripts/bench.py
git commit -m "feat: symbol_id filter in /ask + UI picker + latency benchmark"
git push -u origin day47-symbol-filter
```

PR → **Closes #Day-47 issue** → merge when CI passes & bench workflow green. Move card to **Done**.

---

### ✅ End‑of‑Day 47 Definition

* `/ask` supports optional `symbol_id`; Pinecone filter works.
* Symbol picker limits answers; cards display colored trail.
* Bench P90 latency ≤ 2 s with filter.

*Tomorrow (Day 48):* spin up Beta wait‑list landing page and capture emails.