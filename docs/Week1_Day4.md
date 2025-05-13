# Week 1 — Day 4 (Embedding Pipeline Stub)

> **Target session:** ≈ 2 h     **Focus:** build a one‑off Python script that looks for pages that still have `embedding IS NULL`, calls the OpenAI embedding API, and writes the resulting vector back into Supabase.
>
> **Outcome:** row `id 1` in `pages` will have a 1536‑dimensional vector stored in its `embedding` column, and you’ll prove the column can be queried.

---

## 0 · Pre‑flight

* Confirm `OPENAI_API_KEY` is set in your local `.env` (and **only** there – never committed).
* Optional: export it for current shell → `export OPENAI_API_KEY=$(grep OPENAI_API_KEY .env | cut -d '=' -f2-)`.

---

## 1 · Add dependencies

In `apps/backend/requirements.txt` (or create a dedicated `requirements-scripts.txt`):

```
openai>=1.23
supabase>=2.0
python-dotenv
```

Commit:

```bash
git add apps/backend/requirements.txt
git commit -m "deps: add openai for embedding script"
```

*(Backend image will pick this up next rebuild, but tonight you’ll run the script locally.)*

---

## 2 · Write the seeding script

Create `scripts/embed_seed.py` (new folder if needed):

```python
#!/usr/bin/env python3
"""Embed any pages whose embedding is NULL (up to LIMIT)."""
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
from supabase import create_client

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not (SUPABASE_URL and SUPABASE_KEY and OPENAI_KEY):
    sys.exit("🛑  Set SUPABASE_URL, SUPABASE_ANON_KEY, OPENAI_API_KEY in .env")

sb = create_client(SUPABASE_URL, SUPABASE_KEY)
client = OpenAI(api_key=OPENAI_KEY)

BATCH = 10  # keep costs tiny for now
MODEL = "text-embedding-3-small"

rows = (
    sb.table("pages")
      .select("id, content")
      .is_("embedding", "null")
      .limit(BATCH)
      .execute()
      .data
)
print(f"Embedding {len(rows)} rows…")
for r in rows:
    resp = client.embeddings.create(input=r["content"], model=MODEL)
    vec = resp.data[0].embedding  # list[float]
    sb.table("pages") \
      .update({"embedding": vec}) \
      .eq("id", r["id"]) \
      .execute()
    print(f"· id {r['id']} embedded → len={len(vec)}")
print("✅ Done")
```

Make it executable:

```bash
chmod +x scripts/embed_seed.py
```

Commit script:

```bash
git add scripts/embed_seed.py
git commit -m "feat: embed_seed script fills vector column"
```

---

## 3 · Run & verify

```bash
python scripts/embed_seed.py
```

In Supabase SQL editor:

```sql
select id, embedding[1:3] as preview, floor(vector_norm(embedding)::numeric, 4) as norm
from pages where id = 1;
```

Should show first 3 dims and non‑null vector norm.

---

## 4 · Optional – stub cron in CI (disabled)

Add `.github/workflows/embed-cron.yml`:

```yaml
name: Embed Cron (disabled)
# on:
#   schedule:
#     - cron: '0 3 * * *'  # daily 03:00 UTC
#   workflow_dispatch:
jobs:
  noop:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Cron disabled until prod phase"
```

Commit:

```bash
git add .github/workflows/embed-cron.yml
git commit -m "ci: placeholder cron for embeddings (commented)"
```

---

## 5 · Push branch & PR

```bash
git push --set-upstream origin day4-embed-seed
```

Open PR → link to *Day 4 – Embedding stub* issue → merge after green.

Move board card **“Day 4 – Embedding stub script”** ➜ *Done*.

---

### ✅ End‑of‑Day 4 Definition

* `scripts/embed_seed.py` populates `embedding` for shard 1.
* Manual SQL confirms vector stored & dimension = 1536.
* Placeholder cron workflow exists but is inactive.

*Tomorrow (Day 5):* boot the React shell that fetches `/read` and renders the shard.
