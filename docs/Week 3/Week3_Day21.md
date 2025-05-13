# Week 3 — Day 21 (Sprint Retro & Week 4 Kick‑off)

> **Target session:** 1 h  **Goal:** lock in Week 3 learnings, verify Gift loop KPIs, and prepare the Week 4 board (Full‑Corpus ingest). If time allows, point the nightly embed cron at the 710‑page TSV so it can churn while you sleep.
>
> **Outcome:** `README‑W3.md` has a filled‑in retro; Project board owns a fresh “Week 4 – Full Corpus & Dual Store” column with seed issues; cron path updated.

---

## 1 · Write the Week 3 retrospective

Create **`docs/README‑W3.md`** or append if exists:

```md
## Week 3 Retrospective

### What went well 🎉
- Gift loop (Kafka → Faust → DB) hit < 800 ms end‑to‑end.
- Supabase Realtime pushed timeline updates instantly on multiple tabs.
- Symbol filter UI helped navigation without extra backend queries.

### What puzzled or slowed us 🤔
- Faust image size bloated docker build (500 MB+).
- Race condition when saving + deleting quickly (duplicate Kafka key).
- Tailwind dark‑mode purge required manual rebuild in CI.

### Scope shifts 🔄
- Row‑level security postponed to Week 5 (requires Auth).
- Fancy symbol animations moved to Parking‑Lot.

### Metrics 📊 (average across last 50 asks)
| Metric                    | Value |
|---------------------------|-------|
| /ask latency (median)     | xx ms |
| Prompt tokens (avg)       | xx    |
| Completion tokens (avg)   | xx    |
| Cost per /ask (avg)       | $0.00xx |
| Gift loop latency (95p)   | xx ms |

### Emotional battery 🔋
- Rating: X / 5 – quick wins but streaming pipeline debugging was draining.
```

Commit:

```bash
git add docs/README-W3.md
git commit -m "docs: add Week 3 retrospective"
```

---

## 2 · Create Week 4 Project column & seed issues

### 2.1 New column

Project board → **Add column** → **“Week 4 – Full Corpus & Dual Store”**.

### 2.2 Seed issues (copy‑paste)

| Issue Title                                     | Labels                |
| ----------------------------------------------- | --------------------- |
| Day 22 – Bulk upload 710‑page TSV to `pages`    | week4, backend        |
| Day 23 – PS batch embed → Pinecone store        | week4, backend, infra |
| Day 24 – Dual‑store routing helper              | week4, backend        |
| Day 25 – Search latency benchmark (> 700 pages) | week4, infra          |
| Day 26 – Loading skeleton & paging UI           | week4, frontend       |
| Day 27 – Cron monitor & alert (token cost)      | week4, infra          |
| Day 28 – Retro & Week 5 planning                | week4, docs           |
| Drag each to the Week 4 column.                 |                       |

---

## 3 · Point embed cron at full corpus (optional)

1. Place `corpus_full.tsv` (id, title, content, symbol\_id) in `datasets/`.
2. Edit `scripts/embed_seed.py` default query: replace `limit(1000)` with `limit(None)`.
3. Update cron workflow env var:

```yaml
      - name: set TSV path
        run: echo "TSV_PATH=datasets/corpus_full.tsv" >> $GITHUB_ENV
```

Commit optional tweak:

```bash
git add scripts/embed_seed.py .github/workflows/embed-cron.yml
git commit -m "chore: point embed cron to full corpus TSV"
```

---

## 4 · Push & PR

```bash
git checkout -b day21-retro
git push -u origin day21-retro
```

Open PR → **Closes #Day‑21 issue** → merge when green.
Move Week 3 column to **Done** (archive if desired).

---

### ✅ End‑of‑Day 21 Definition

* Week 3 retro committed.
* Week 4 column + seed issues ready.
* (Optional) embed cron now targets full corpus.

**Week 3 sprint complete.** Next stop: ingest 710 pages and test Pinecone dual‑store routing!
