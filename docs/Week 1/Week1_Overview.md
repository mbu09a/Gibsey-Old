# Week 1 Overview — “Walking‑Skeleton” Sprint

## Sprint Goal

Lock scope and bring up a minimal stack able to serve **one hard‑coded shard** through the full loop `React → FastAPI → Supabase → React` in **≤ 2 seconds**.

---

## Daily Plan

### Day 0 – Kick‑off & Scope‑Freeze *(Sun, 1–2 h)*

* **Deliverables**

  * `README‑W1.md` with sprint checklist
  * GitHub Project board & labels
  * `.env.example` with required secrets
* **Guardrails** – skip Kafka, Faust, Tailwind polish, pgvector tuning (move to Week 2+)

---

### Day 1 – Repo & CI Skeleton *(Mon, 2–3 h)*

* **Deliverables**

  * Monorepo scaffold `apps/frontend`, `apps/backend`, `infra/compose.yaml`
  * GitHub Actions running `docker compose up` + basic lint
* **Tip** – any green CI check by bedtime (tests may be placeholders)

---

### Day 2 – Backend Bootstrap *(Tue, ≈ 2 h)*

* **Deliverables**

  * FastAPI route `GET /health → {"status":"ok"}`
  * Pydantic settings via `.env`
  * Backend Dockerfile & compose service
* **Tip** – keep everything in a single `main.py` for now

---

### Day 3 – Database Up *(Wed, 2–3 h)*

* **Deliverables**

  * Supabase project
  * `pages` table (`id`, `title`, `content`, `symbol_id`)
  * `pgvector` extension enabled
  * *Optional* local Postgres mirror via Docker
* **Tip** – insert **one** shard manually and query it from FastAPI

---

### Day 4 – Embedding Pipeline Stub *(Thu, ≈ 2 h)*

* **Deliverables**

  * `scripts/embed_seed.py` — fetch NULL embeddings, call OpenAI, store vector
  * Cron GitHub Action (commented‑out)
* **Tip** – hard‑code model `text‑embedding‑3‑small`; ignore ONNX for now

---

### Day 5 – Frontend Shell *(Fri, 1–2 h)*

* **Deliverables**

  * Vite + React page
  * “Fetch Shard” button → `/read?id=1`, renders title & content
* **Tip** – use Tailwind CDN; defer shadcn until Week 2

---

### Day 6 – End‑to‑End Round‑Trip *(Sat, \~ 4 h)*

* **Deliverables**

  * `POST /ask` returns stub answer
  * React form posts question & displays JSON
  * Console logs round‑trip latency
* **Tip** – celebrate: minimal **Read → Ask** loop is alive

---

### Day 7 – Vault Stub & Retro *(Sun, 3 h + 30 min retro)*

* **Deliverables**

  * `vault` table + `/vault/save` inserts record
  * 30‑min retrospective — wins, blockers, scope shifts
* **Tip** – if tired, stub endpoint but create DB table so schema is locked

---

## Daily Ritual

1. **Pre‑session (5 min)** — read yesterday’s commit; open *one* new issue.
2. **Work blocks** — 45 min Pomodoro → commit runnable slices.
3. **Wrap‑up** — push branch; add 2‑sentence progress note to issue.

### Stretch Goals (if ahead)

* Enable Supabase Row‑Level Security for `vault`.
* Add Jest/Vitest smoke test for `/health`.

> **Scope discipline:** any ⚠️ feature moves to **Week 2+**. If a task slips, drag it to the next day—never into a late‑night doom‑spiral.

Finish Week 1 with a Docker‑orchestrated skeleton you can click through—that’s all the foundation you need!

