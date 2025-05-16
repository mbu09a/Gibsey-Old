# Week 2 — Day 8 (Bulk Embed 33 Shards)

> **Target session:** ≈ 2 h  **Goal:** store real embeddings for every Author’s Preface shard and wire a nightly cron.
>
> **Outcome:** `pages.embedding` is non‑NULL for all 33 rows; `scripts/embed_seed.py --dry` prints cost; cron workflow is enabled.

---

## 1 · Expand `embed_seed.py`

### 1.1 Add CLI flags & batching

```python
#!/usr/bin/env python3
"""Embed any pages whose embedding is NULL.
usage: embed_seed.py [--dry] [--batch 10]
"""
import argparse, os, sys, time, math, json
from dotenv import load_dotenv
from openai import OpenAI, APIError
from supabase import create_client

MODEL = "text-embedding-3-small"
PRICE_PER_1K = 0.00002  # USD for small model

load_dotenv()
SB_URL = os.getenv("SUPABASE_URL")
SB_KEY = os.getenv("SUPABASE_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not (SB_URL and SB_KEY and OPENAI_KEY):
    sys.exit("🛑  Missing env vars (SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY)")

sb = create_client(SB_URL, SB_KEY)
client = OpenAI(api_key=OPENAI_KEY)

parser = argparse.ArgumentParser()
parser.add_argument("--dry", action="store_true", help="don’t call OpenAI, just estimate cost")
parser.add_argument("--batch", type=int, default=10)
args = parser.parse_args()

rows = sb.table("pages").select("id, content").is_("embedding", "null").limit(1000).execute().data
print(f"🔎 {len(rows)} rows need embeddings")

total_tokens = 0
for i in range(0, len(rows), args.batch):
    chunk = rows[i : i + args.batch]
    texts = [r["content"] for r in chunk]
    if args.dry:
        # rough 1 token ≈ 4 chars
        tokens = sum(math.ceil(len(t) / 4) for t in texts)
        total_tokens += tokens
        continue
    backoff = 1
    while True:
        try:
            resp = client.embeddings.create(model=MODEL, input=texts)
            break
        except APIError as e:
            print(f"OpenAI error → retry in {backoff}s")
            time.sleep(backoff)
            backoff = min(backoff * 2, 60)
    for r, emb in zip(chunk, resp.data):
        sb.table("pages").update({"embedding": emb.embedding}).eq("id", r["id"]).execute()
        total_tokens += resp.usage.total_tokens
        print(f"· id {r['id']} embedded (dims={len(emb.embedding)})")

usd = (total_tokens / 1000) * PRICE_PER_1K
print(json.dumps({"tokens": total_tokens, "usd_estimate": round(usd, 4)}, indent=2))
```

Make executable:

```bash
chmod +x scripts/embed_seed.py
```

### 1.2 Update deps

Append to `apps/backend/requirements.txt` if missing:

```
openai>=1.23
```

*(backend image will pick it up next build.)*

---

## 2 · Dry‑run cost estimate

```bash
python scripts/embed_seed.py --dry
# → prints tokens and ~$ cost (should be a few cents)
```

Commit:

```bash
git add scripts/embed_seed.py apps/backend/requirements.txt
git commit -m "feat: bulk embedding script with --dry and batching"
```

---

## 3 · Embed for real & verify

```bash
python scripts/embed_seed.py --batch 10
```

SQL check:

```sql
select count(*) from pages where embedding is null;  -- expect 0
```

---

## 4 · Enable nightly cron

Edit `.github/workflows/embed-cron.yml`:

```yaml
name: Embed Cron
on:
  schedule:
    - cron: '0 3 * * *'
  workflow_dispatch:
```

Add repo secrets `SUPABASE_URL`, `SUPABASE_KEY`, `OPENAI_API_KEY` via **Settings → Secrets & Variables → Actions**.
Commit:

```bash
git add .github/workflows/embed-cron.yml
git commit -m "ci: enable nightly embedding cron"
```

---

## 5 · Rebuild backend image (picks up openai lib)

```bash
docker compose -f infra/compose.yaml build backend && docker compose up -d backend
```

---

## 6 · Push branch & PR

```bash
git checkout -b day8-embed
git push -u origin day8-embed
```

Open PR → **Closes #Day‑8 issue** → wait for green CI → merge.
Move project card to **Done**.

---

### ✅ End-of-Day 8 Definition

* 33 `pages` rows have non‑NULL `embedding` vectors.
* Script supports `--dry` and batching.
* Nightly cron enabled (secrets added).

*Tomorrow (Day 9):* implement pgvector similarity helper and its tests.
