# Week 4 — Day 23 (Batch Embed → Pinecone)

> **Target session:** ≈ 3 h  **Goal:** configure a Pinecone index, extend `embed_seed.py` to upsert embeddings in 100‑row batches, and run the script once to cover all 710 new pages. Enable the nightly embed cron.
>
> **Outcome:** Pinecone index holds 710 new vectors (total 743), `/ask` dual‑store routing can query it tomorrow, and embed‑cron is live.

---

## 1 · Create Pinecone index

1. Sign in to **app.pinecone.io** → **Create Index**.
2. Name: **`gibsey-pages`**.
   ‑ **Dimension:** `1536`  (matches `text‑embedding‑3‑small`).
   ‑ **Metric:** `cosine`.
   ‑ **Pods:** *Starter* (1 pod, 1 replica is fine for dev).
   ‑ Wait until Status = *Ready*.
3. Copy **Environment** (e.g. `gcp-starter`), **Index name**, and generate an **API key**.

Add these to repo secrets & local `.env`:

```env
PINE_ENV=gcp-starter
PINE_API_KEY=xxxxxxxxxxxxxxxxxxxx
PINE_INDEX=gibsey-pages
```

---

## 2 · Install Pinecone client in backend image

Append to `apps/backend/requirements.txt`:

```
pinecone-client>=3.0
```

---

## 3 · Update `scripts/embed_seed.py` for Pinecone

Key changes:

```python
from pinecone import Pinecone, ServerlessSpec

PC = Pinecone(api_key=os.getenv("PINE_API_KEY"))
index = PC.Index(os.getenv("PINE_INDEX"),
                 spec=ServerlessSpec(cloud="gcp", region="us-west1"))

BATCH = args.batch  # default 100 today
...
upserts = [(str(r["id"]), emb, {"symbol_id": r["symbol_id"]})
           for r, emb in zip(chunk, resp.data)]
index.upsert(upserts)
print(f"↑ upserted {len(upserts)} to Pinecone")
```

Ensure you still update `pages.embedding` locally for pgvector fallback.

---

## 4 · Run embed for real (once)

```bash
python scripts/embed_seed.py --batch 100
```

Console should show 710 embeddings and cost estimate.  Check Pinecone dashboard → **Vectors = 743**.

---

## 5 · Enable embed‑cron

Edit `.github/workflows/embed-cron.yml`:

```yaml
on:
  schedule:
    - cron: "0 4 * * *"   # daily 04:00 UTC
  workflow_dispatch:
```

Remove any `if: false` guard so it runs nightly.

---

## 6 · Rebuild backend for client deps

```bash
docker compose -f infra/compose.yaml build backend && docker compose up -d backend
```

---

## 7 · Smoke query with Pinecone SDK

```python
from pinecone import Pinecone
pc = Pinecone(api_key="...", environment="gcp-starter")
idx = pc.Index("gibsey-pages")
print(idx.describe_index_stats())
```

Should show `total_vector_count: 743`.

---

## 8 · Commit & PR

```bash
git checkout -b day23-pinecone-embed
git add apps/backend/requirements.txt scripts/embed_seed.py .github/workflows/embed-cron.yml
# do NOT commit TSV or .env
git commit -m "feat: batch embed 710 pages to Pinecone and activate nightly cron"
git push -u origin day23-pinecone-embed
```

PR → **Closes #Day‑23 issue** → merge when CI green; move card to **Done**.

---

### ✅ End‑of‑Day 23 Definition

* Pinecone index `gibsey-pages` holds **743** vectors.
* `scripts/embed_seed.py` upserts in batches; cost/log output works.
* GitHub nightly cron enabled for incremental embeddings.

*Tomorrow (Day 24):* implement dual‑store routing helper and update `/ask` to query Pinecone when corpus > 500.