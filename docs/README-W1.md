# Week 1 — Walking‑Skeleton Sprint

Owner | mbu09a
--- | ---
Sprint Goal | Stand up Docker‑compose stack that serves **one** shard via `/read`, callable from React shell, ≤2 s round‑trip.
Duration | 7 days (5/12/2025-5/19/2025)

## Daily Checklist
- [x] Day 0 – Kickoff & Scope‑freeze
- [x] Day 1 – Repo & CI skeleton
- [ ] Day 2 – Backend bootstrap
- [ ] Day 3 – Database up
- [ ] Day 4 – Embedding stub
- [ ] Day 5 – Frontend shell
- [ ] Day 6 – End‑to‑end loop
- [ ] Day 7 – Vault stub + retro

## "Definition of Done" (Week 1)
1. `docker compose up` brings up FastAPI + Supabase + React without errors.
2. GET `/read?id=1` returns hard‑coded shard JSON.
3. React button renders that shard in browser.