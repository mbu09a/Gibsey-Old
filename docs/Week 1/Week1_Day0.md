# Week 1 — Day 0 (Kickoff & Scope‑Freeze)

> **Goal for the evening (≤ 2 h):** freeze scope, create the Week‑1 groundwork in‑repo, and publish a visible checklist so every other task has a home.

---

## 1. Create / update monorepo

```bash
# If starting from scratch
mkdir gibsey && cd gibsey

# OR if cloning existing code
git clone https://github.com/<your‑user>/gibsey.git && cd gibsey

git checkout -b week1
mkdir -p apps/frontend apps/backend infra scripts docs
```

*House‑rule: every new feature lives on its own feature‑branch **inside** `week1` and merges via PR.*

---

## 2. Add README‑W1.md

Paste the block below into `README-W1.md` (**replace «NAME» with your GH handle**):

```md
# Week 1 — Walking‑Skeleton Sprint

Owner | «NAME»
--- | ---
Sprint Goal | Stand up Docker‑compose stack that serves **one** shard via `/read`, callable from React shell, ≤2 s round‑trip.
Duration | 7 days (…‑…)

## Daily Checklist
- [ ] Day 0 – Kickoff & Scope‑freeze
- [ ] Day 1 – Repo & CI skeleton
- [ ] Day 2 – Backend bootstrap
- [ ] Day 3 – Database up
- [ ] Day 4 – Embedding stub
- [ ] Day 5 – Frontend shell
- [ ] Day 6 – End‑to‑end loop
- [ ] Day 7 – Vault stub + retro

## "Definition of Done" (Week 1)
1. `docker compose up` brings up FastAPI + Supabase + React without errors.
2. GET `/read?id=1` returns hard‑coded shard JSON.
3. React button renders that shard in browser.
```

Commit:

```bash
git add README-W1.md
git commit -m "docs: add Week 1 README skeleton"
```

---

## 3. Add `.env.example`

Create `.env.example` in repo root:

```env
# ==== Runtime Secrets (copy to .env locally) ====
OPENAI_API_KEY=
SUPABASE_URL=
SUPABASE_ANON_KEY=
# DB
POSTGRES_USER=gibsey
POSTGRES_PASSWORD=secret
POSTGRES_DB=gibsey
```

Commit:

```bash
git add .env.example
git commit -m "chore: scaffold env template"
```

---

## 4. GitHub Project / Issue board

1. Go to **Repo → Projects → “New project” → Board**.
2. Title: `Week 1 – Walking‑Skeleton`.
3. Columns: `Backlog`, `In‑Progress`, `Done`, `Parking‑Lot`.
4. Add labels in repo Settings → Labels:

   * `week1`
   * `backend`
   * `frontend`
   * `infra`
   * `docs`

### Seed issues (copy / paste)

| Title                         | Label(s)                 |
| ----------------------------- | ------------------------ |
| Day 1 – Repo & CI skeleton    | week1, infra             |
| Day 2 – FastAPI health route  | week1, backend           |
| Day 3 – Supabase pages table  | week1, backend           |
| Day 4 – Embedding stub script | week1, backend           |
| Day 5 – React shell           | week1, frontend          |
| Day 6 – E2E latency test      | week1, frontend, backend |
| Day 7 – Vault table & retro   | week1, backend, docs     |

Drag all to **Backlog**.

---

## 5. Set up basic CI (placeholder)

Add `.github/workflows/ci.yml`:

```yaml
name: CI
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: stub
        run: echo "🧹  CI placeholder – real lint hooks land Day 1"
```

Commit & push upstream:

```bash
git add .github/workflows/ci.yml
git commit -m "ci: placeholder workflow"
git push --set-upstream origin week1
```

---

## 6. Personal Kanban + calendar block

Book **45‑min** nightly slot (Mon‑Sat) in your calendar titled `Gibsey Week1`. Treat it as immovable.

---

### ✅ End-of‑Day 0 definition:

* Repo has Week 1 branch, folder scaffold, README‑W1.md, `.env.example`, CI placeholder.
* GitHub Project board seeded.
* Personal time blocks scheduled.

Commit count should be **≥ 3**; push, then close “Day 0” issue as *Done*.