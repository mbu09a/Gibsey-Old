# Week 2 Overview — “Core RAG Loop” Sprint (May 13 → May 19, 2025)

> **Sprint Goal:** turn the walking skeleton into a real **Read → Ask → Receive → Save** loop using OpenAI embeddings + GPT‑4o, and surface a minimal Vault timeline.
>
> **Definition of Done**
>
> 1. All 33 *Author’s Preface* shards embedded.
> 2. `/ask` answers via pgvector similarity + GPT‑4o.
> 3. React shows answers *and* a chronological Vault list.
> 4. End‑to‑end ask round‑trip **≤ 2 s**.

---

## Daily Plan

### Day 8 — Embed 33 Shards *(Tue 5/13, ≈ 2 h)*

* **Deliverables**

  * Enhance `scripts/embed_seed.py`:

    * `--dry` flag prints token & cost estimate without API calls.
    * Bulk‑embed rows where `embedding IS NULL` (batch 10, exp. back‑off).
  * Un‑comment nightly cron (`embed-cron.yml`) to run at 03:00 UTC.
* **Guardrail** – keep model `text-embedding-3-small`; log estimated \$.

---

### Day 9 — Vector Search Helper *(Wed 5/14, ≈ 2 h)*

* **Deliverables**

  * `app/vector.py` → `similar_pages(text: str, k: int = 3)` returns **`[{id, content, score}]`** using `1 - (embedding <=> query)`.
  * Pytest with tiny fake matrix to verify ordering.
* **Tip** – single query; avoid extra round‑trip for content fetch.

---

### Day 10 — Real RAG in `/ask` *(Thu 5/15, ≈ 3 h)*

* **Deliverables**

  * Build context prompt from top‑3 snippets → call GPT‑4o.
  * Add headers: `X-Tokens-Prompt`, `X-Tokens-Comp`, `X-Cost-USD`, `X-Latency-MS`.
  * Fallback: if LLM fails, return stub answer + 503.
* **Perf check** – avg total latency < 1.5 s.

---

### Day 11 — Vault Timeline Read‑View & Tailwind Swap *(Fri 5/16, ≈ 2 h)*

* **Deliverables**

  * Backend `/vault/list?page=1&limit=20` (pagination ready).
  * React `VaultTimeline` component under Ask form; auto‑scroll to latest.
  * Swap Tailwind CDN → full Tailwind + `shadcn/ui` install (baseline card styles).

---

### Day 12 — Latency & Cost Instrumentation *(Sat 5/17, ≈ 1 h light)*

* **Deliverables**

  * Timing wrapper logs JSON to stdout **and** `logs/ask-YYYY-MM-DD.jsonl`.
  * `$` cost per request (tokens × price) included in log.

---

### Day 13 — Code‑Quality Pass *(Sun 5/18, ≈ 3 h deep)*

* **Deliverables**

  * Set up **pre‑commit**: Ruff, Black, isort, ESLint — runs on staged files.
  * Fix all lint / format issues (mechanical only; no refactors).

---

### Day 14 — Retro + Week 3 Planning *(Mon 5/19, ≈ 1 h)*

* **Deliverables**

  * Add Retro section to `README-W2.md` (wins, blockers, latency, cost).
  * Create Week 3 issues & column.
  * **If ahead**: scaffold Redpanda topic & stub Faust consumer.

---

## Daily Ritual (unchanged)

1. **Pre‑session** – skim previous commit; open **one** issue.
2. **45‑min Pomodoros** – ship runnable slices; commit small.
3. **Wrap‑up** – push branch; log 2‑sentence progress note.

### Stretch Goals

* Supabase Row‑Level Security on `vault` now that read‑view exists.
* Jest/Vitest tests for React components.

> **Scope rule:** any Redpanda/Faust work or extra UI polish rolls into Week 3 if it endangers latency or stability.
