# Week 4 Overview — “Full Corpus & Dual‑Store” Sprint (Days 22 – 28)

> **Sprint Goal:** load the entire 710‑page corpus, embed it into a scalable vector store (Pinecone or Astra DB), and introduce **dual‑store routing** so `/ask` can seamlessly query both pgvector (legacy) and the external index. Round‑trip latency must stay ≤ 2 s.
>
> **Definition of Done**
>
> 1. `pages` table contains all 710 rows; `symbol_id` populated.
> 2. Nightly `embed-cron` writes new embeddings to Pinecone (or Astra).
> 3. `/ask` routes: if corpus > 500 rows → query Pinecone; else → pgvector.
> 4. Search benchmark script shows **P90 latency < 1.2 s** for a query against full corpus.
> 5. Front‑end displays loading skeleton + paging for > 20 search hits.

---

## Daily Plan

| Day               | Focus                            | Deliverables                                                                                            | Guardrails                                      |
| ----------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| **22 (Tue 5/27)** | **Bulk TSV import**              | Load `corpus_full.tsv` (710 rows) into `pages`; quick spot‑check counts and symbol distribution.        | No embeddings yet.                              |
| **23 (Wed 5/28)** | **Batch embed → Pinecone**       | Configure Pinecone index; adapt `embed_seed.py` to upsert in 100‑row batches; run once locally.         | Keep `dim=1536`, cosine metric, `pods=starter`. |
| **24 (Thu 5/29)** | **Dual‑store routing helper**    | `app/vector.py` detects corpus size; if >500 → query Pinecone; else pgvector. Unit test mocks both.     | Fallback to pgvector on Pinecone error.         |
| **25 (Fri 5/30)** | **Latency benchmark script**     | `scripts/bench.py` fires 100 random questions; outputs P50/P90 latency + cost CSV; CI job runs on PR.   | Fail CI if P90 > 1.5 s.                         |
| **26 (Sat 5/31)** | **Loading skeleton & paging UI** | React `SearchResults` shows skeleton while `/ask` pending; add “Load more” for >20 hits.                | No infinite scroll yet.                         |
| **27 (Sun 6/1)**  | **Cron monitor + alert**         | GitHub Action checks embed‑cron duration & failure; sends Slack/Webhook alert if run > 30 min or fails. | Use repo secret `SLACK_WEBHOOK_URL`.            |
| **28 (Mon 6/2)**  | **Retro & Week 5 planning**      | Write `README-W4.md` retro; seed Week 5 board (Auth & RLS).                                             | Optional: tail cost charts in Grafana.          |

---

### Stretch Goals

* Switch Pinecone pod to on‑demand HNSW if latency > 800 ms.
* Add simple retry + exponential back‑off to embed‑cron.
* Display token‑cost per search result batch in UI footer.

> **Scope rule:** auth flows and RLS **must stay in Week 5**; no user login work this week unless the corpus ingest finishes early and latency is green.