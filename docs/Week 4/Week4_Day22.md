# Week 4 — Day 22 (Bulk Import 710‑Page Corpus)

> **Target session:** ≈ 2 h  **Goal:** ingest the full TSV corpus (710 pages) into the `pages` table with proper `symbol_id`s. No embeddings yet—just raw rows. Verify counts and prep the dataset for tomorrow’s Pinecone batch embed.
>
> **Outcome:** `pages` now has **710 + 33 = 743** total rows; `select count(*)` matches; spot‑check a few IDs.

---

## 1 · Prepare the TSV file

Assume you have `datasets/corpus_full.tsv` in the repo root with header:

```
id	title	content	symbol_id
```

*(If not, create/export it first—each field tab‑separated.)*
Add file to `.gitignore` if > 5 MB:

```bash
echo "datasets/*.tsv" >> .gitignore
```

---

## 2 · Quick schema sanity

Ensure `pages` has matching columns:

```sql
alter table pages
  add column if not exists title text,
  add column if not exists content text,
  add column if not exists symbol_id int default 1;
```

Run once in Supabase SQL editor.

---

## 3 · Import via Supabase `copy` (fast)

1. In SQL editor choose **“SQL” → “New query”**.
2. Paste:

```sql
-- adjust bucket/path if you upload to Supabase Storage
create table if not exists staging_pages (like pages);
copy staging_pages (id,title,content,symbol_id)
from 'https://YOUR-PROJECT.supabase.co/storage/v1/object/public/imports/corpus_full.tsv'
with (format csv, header true, delimiter E'\t');

insert into pages (id,title,content,symbol_id)
select * from staging_pages
on conflict (id) do update set
  title=excluded.title,
  content=excluded.content,
  symbol_id=excluded.symbol_id;

drop table staging_pages;
```

*(Upload TSV to Supabase Storage → `imports` bucket first.)*

If you prefer **local psql** inside the Postgres container:

```bash
docker exec -i gibsey-dev-stack-db-1 psql -U postgres -d gibsey < datasets/corpus_full.tsv
```

Adjust `\copy` command accordingly.

---

## 4 · Verify counts

In SQL editor:

```sql
select count(*) as total, max(id) as max_id from pages;
```

Expect `total = 743`, `max_id >= 710`.
Random spot‑check:

```sql
select id,title,symbol_id from pages where id in (45, 350, 689);
```

---

## 5 · Update embed‑cron ENV (no embeddings today)

Edit **`.github/workflows/embed-cron.yml`** but leave `if: false` to keep it disabled until Day 23. Just set:

```yaml
env:
  TSV_PATH: datasets/corpus_full.tsv
```

Commit changes.

---

## 6 · Commit & PR

```bash
git checkout -b day22-bulk-import
git add datasets/.gitignore .github/workflows/embed-cron.yml
# TSV is ignored, only helper changes tracked
git commit -m "feat: import full 710-page corpus into pages table"
git push -u origin day22-bulk-import
```

Open PR → **Closes #Day-22 issue** → merge when green.
Move board card to **Done**.

---

### ✅ End‑of‑Day 22 Definition

* `pages` row count = **743** (33 preface + 710 corpus).
* Spot‑checked titles & symbol IDs correct.
* Embed cron prepared but still paused.

*Tomorrow (Day 23):* configure Pinecone and batch‑embed the new rows.