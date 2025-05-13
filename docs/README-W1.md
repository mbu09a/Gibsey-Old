# Week 1 — Walking‑Skeleton Sprint

Owner | mbu09a
--- | ---
Sprint Goal | Stand up Docker‑compose stack that serves **one** shard via `/read`, callable from React shell, ≤2 s round‑trip.
Duration | 7 days (5/12/2025-5/19/2025)

## Daily Checklist
- [x] Day 0 – Kickoff & Scope‑freeze
- [x] Day 1 – Repo & CI skeleton
- [x] Day 2 – Backend bootstrap
- [x] Day 3 – Database up
- [x] Day 4 – Embedding stub
- [x] Day 5 – Frontend shell
- [x] Day 6 – End‑to‑end loop
- [x] Day 7 – Vault stub + retro

## "Definition of Done" (Week 1)
1. `docker compose up` brings up FastAPI + Supabase + React without errors.
2. GET `/read?id=1` returns hard‑coded shard JSON.
3. React button renders that shard in browser.

## Week 1 Retrospective

### What went well?
- Docker Compose setup was smooth and reliable throughout the project
- FastAPI and Supabase integration was straightforward to implement
- React frontend development was quick with Vite's fast refresh
- The entire end-to-end flow was completed in the planned timeframe
- Latency targets were easily met with current implementation

### What puzzled or slowed you?
- Initial Supabase setup required some extra time to understand properly
- The mock embedding workflow could use better documentation
- TypeScript type definitions could be more robust in the frontend

### Scope changes?
- No major scope changes, all Week 1 tasks were completed
- Stretch goals for OpenAI integration deferred to Week 2
- Full vault UI and retrieval functionality moved to Week 2

### Latency check:
- `/ask` endpoint latency: ~50ms (stub implementation)
- End-to-end round trip: ~100ms (well under 2s target)

### Emotional battery:
- Rating: 4/5 - Good progress with minimal blockers