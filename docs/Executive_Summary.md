# Executive Summary – Gibsey MVP (Last MVP)

> **Prime directive:** ship a *single*, no‐redo MVP that lets a reader **Read → Ask → Receive → Save** a shard in < 2 s. Start with 33 shards & 2 symbols—design every piece so you can scale to 710 pages and 16 symbols without re‑platforming.

---

## 0 · Snapshot

A logged‑in user can…

1. **Read** a curated narrative shard (initially *An Author’s Preface* – 33 shards).
2. **Ask** a question about that shard.
3. **Receive** an AI answer in‑context.
4. **Save** the Q\&A to a personal **Vault** timeline.

**Stack (v1):** FastAPI │ React + Tailwind │ PostgreSQL + `pgvector` │ OpenAI embeddings & GPT‑4o.
**Scale path:** swap/augment stores (Astra DB or Pinecone), add Redpanda + Faust event spine, expand to full Corpus & QDPI modes.

---

## 1 · Vision & Core Goals

* Recursive, multi‑layer storytelling driven by symbolic embeddings.
* **Personal AI reading / writing interface** (the reader is part‑author).
* Implement **QDPI** primitives: **Read, Write, Index, Dream**.
* One stable foundation—*no more migrations*.
* < 2 s round‑trip for Read → Ask → Receive.
* Launch small (33 shards) but architect for 710+ pages & 16 symbols.
* UI embeds Corpus symbols from day one.

---

## 2 · Key Personas & Needs

| Persona           | Core Need                                 |
| ----------------- | ----------------------------------------- |
| **The Seeker**    | Guided exploration & meaning‑making.      |
| **The Archivist** | Save / organise Q\&A threads (Vault).     |
| **The Creator**   | Remix or extend narrative via AI prompts. |

All require: *intuitive nav*, *relevant answers*, *reliable history*.

---

## 3 · Architecture / Tech Stack (v1 focus)

* **Frontend:** `React (Vite)` + Tailwind *(shadcn/UI & lucide‑react : Week 2)*
* **Backend API:** `FastAPI` + Pydantic
* **Auth & Users:** Supabase
* **Data (relational / proto‑vector):** `PostgreSQL` + `pgvector`
* **AI Embeddings / LLM:** OpenAI `text‑embedding‑3‑small` & GPT‑4o
* **CI/CD:** GitHub Actions

> **Parking for scale / later sprints:** Redpanda Kafka, Faust agents, Apache Airflow, Astra DB | Pinecone, Docker → Kubernetes, Prometheus → Grafana.

---

## 4 · Roadmap (Milestone cadence)

| Week / Day   | Deliverable                                                      | Notes                                                              |
| ------------ | ---------------------------------------------------------------- | ------------------------------------------------------------------ |
| **W1 D0**    | **Lock scope / repo skeleton**                                   | Monorepo, Docker, CI stub                                          |
| **W1 D7**    | **Walking skeleton up**                                          | FastAPI + Supabase + React shell via Docker Compose                |
| **W2 D14**   | **Core RAG loop**                                                | 33 shards embedded, `/read` & `/ask` endpoints, UI renders answers |
| **W3 D21**   | **Gift loop + Vault v1**                                         | Save Q\&A via event spine (Kafka + Faust), realtime vault view     |
| **W4 D28**   | **Full corpus ingest**                                           | 710 pages, dual‑store routing (pgvector ↔︎ Pinecone/Astra)         |
| **W5 D35**   | **UX polish + Auth**                                             | Mobile tweaks, Supabase Auth, RLS, JWT                             |
| **W6 D42**   | **Alpha launch**                                                 | Deploy (Fly.io / Render), monitoring online                        |
| **Post‑MVP** | Vault edit/delete, 16 symbols & trails, QDPI Index & Dream modes |                                                                    |

---

## 5 · Risks & Open Questions

1. **Product definition:** reader app vs. symbolic AGI playground? *(clarify in W1 retro)*
2. **Vector store at scale:** stay pgvector? migrate to Cassandra 5 serverless (Astra) or Pinecone?
3. **Latency guardrail:** can < 2 s hold with 710 pages + external LLM?
4. **Symbolic UX logic:** final mapping of 16 symbols & orientations to QDPI states.
5. **Token / cost growth:** OpenAI usage as corpus & users expand.

---

## 6 · Parking‑Lot Ideas (to revisit post‑MVP)

* **DreamRIA** standalone dream agent.
* 33‑shard ritual intro as separate interactive sequence.
* TNAs letting users become agents/authors.
* Multi‑agent chat via MCP characters.
* TTS narration for accessibility.
* Shared Vault & community annotation layer.
* Flutter front‑end option if mobile priority spikes.