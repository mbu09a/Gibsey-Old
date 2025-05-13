# Week 3 — Gift Loop & Vault UX Sprint

Owner | mbu09a
--- | ---
Sprint Goal | Introduce the **Gift loop** (event‑driven save pipeline) and upgrade the Vault into a live, editable timeline with symbol‑aware UI.
Duration | 7 days (Days 15 – 21)

## Daily Checklist
- [ ] Day 15 – Kafka Topic
- [ ] Day 16 – Faust Consumer
- [ ] Day 17 – Realtime Vault Update
- [ ] Day 18 – Delete / Edit Endpoints
- [ ] Day 19 – Symbol Chip UI
- [ ] Day 20 – Dark‑Mode Theme & Mobile Polish
- [ ] Day 21 – Retro & Week 4 Setup

## "Definition of Done" (Week 3)
1. "Save to Vault" publishes a `gift_events` message → Redpanda → Faust consumer persists it.
2. Frontend receives realtime update (poll or Supabase channel) without page refresh.
3. Vault entries support **delete** and **edit**.
4. Corpus symbols render as colored chips alongside each entry.
5. End‑to‑end latency **≤ 2 s** from button‑click to timeline update.

## Week 3 Retrospective

### What went well?

### What puzzled or slowed you?

### Scope changes?

### Latency check:

### Emotional battery: 