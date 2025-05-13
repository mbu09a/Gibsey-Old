# Week 2 — Day 9 (Vector Search Helper)

> **Target session:** ≈ 2 h  **Goal:** add a reusable helper that returns the top‑k most similar shards to a query string, plus a Pytest proving it works.
>
> **Outcome:** `app/vector.py` exposes `similar_pages(text, k=3) → List[dict]` and a test passes with mocked embeddings.

---

## 1 · Create `app/vector.py`

```python
from typing import List, Dict
from supabase import Client
from .db import Supabase
from openai import OpenAI

MODEL = "text-embedding-3-small"
client = OpenAI()


def _embed(text: str) -> List[float]:
    """Return OpenAI embedding vector for the query string."""
    resp = client.embeddings.create(model=MODEL, input=text)
    return resp.data[0].embedding


def similar_pages(query: str, k: int = 3) -> List[Dict]:
    """Return top‑k pages ordered by cosine similarity."""
    vec = _embed(query)
    sb: Client = Supabase.client()
    rows = (
        sb.rpc(
            "match_pages",  # we’ll create this Postgres function below
            {"query_embedding": vec, "match_k": k},
        )
        .execute()
        .data
    )
    return rows  # [{id, title, content, score}]
```

### 1.1  Postgres helper function (run in Supabase SQL editor)

```sql
-- match_pages(query_embedding float8[], match_k int)
create or replace function match_pages(query_embedding vector, match_k int = 3)
returns table (
  id        bigint,
  title     text,
  content   text,
  score     float
) language sql stable as $$
  select id, title, content,
         1 - (embedding <=> query_embedding) as score
  from pages
  order by embedding <=> query_embedding
  limit match_k;
$$;
```

This avoids sending a huge vector in plain SQL each time.

---

## 2 · Unit test with Pytest

`apps/backend/tests/test_vector.py`:

```python
import pytest
from app.vector import similar_pages

class DummyEmbed:
    def __init__(self):
        # deterministic small vectors for 3 pages
        self.vectors = {
            "q1": [0.9, 0.1],
        }
    def create(self, **kwargs):
        class R:  # minimal stub
            data = [type("E", (), {"embedding": self.vectors["q1"]})]
        return R()


def test_similar_pages(monkeypatch):
    # monkeypatch OpenAI client inside vector.py
    import app.vector as v
    v.client = DummyEmbed()

    results = v.similar_pages("q1", k=1)
    assert len(results) == 1
    assert "score" in results[0]
```

Add Pytest to requirements if missing.

---

## 3 · CI update (backend‑lint job)

```yaml
      - name: tests
        run: |
          pip install pytest
          pytest -q apps/backend/tests
```

Commit:

```bash
git add app/vector.py apps/backend/tests/test_vector.py .github/workflows/ci.yml
git commit -m "feat: pgvector similarity helper + test"
```

---

## 4 · Manual smoke test

```python
python - <<'PY'
from app.vector import similar_pages
print(similar_pages("Who is the mysterious Author?", k=3))
PY
```

Should return a list of 3 dicts with `score` ≈ 0‑1.

---

## 5 · Push branch & PR

```bash
git checkout -b day9-vector-helper
git push -u origin day9-vector-helper
```

Open PR → **Closes #Day‑9 issue** → merge after green CI.
Move project card to **Done**.

---

### ✅ End‑of‑Day 9 Definition

* `similar_pages` returns top‑k rows ordered by cosine similarity.
* Unit test passes in CI.
* Postgres `match_pages` function deployed.

*Tomorrow (Day 10):* wire this helper into `/ask` and start generating real GPT‑4o answers.
