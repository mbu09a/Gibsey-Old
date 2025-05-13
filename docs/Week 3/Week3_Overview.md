# Week 3 Overview — “Gift Loop & Vault UX” Sprint (Days 15 – 21)

> **Sprint Goal:** introduce the **Gift loop** (event‑driven save pipeline) and upgrade the Vault into a live, editable timeline with symbol‑aware UI.
>
> **Definition of Done**
>
> 1. “Save to Vault” publishes a `gift_events` message → Redpanda → Faust consumer persists it.
> 2. Frontend receives realtime update (poll or Supabase channel) without page refresh.
> 3. Vault entries support **delete** and **edit**.
> 4. Corpus symbols render as colored chips alongside each entry.
> 5. End‑to‑end latency **≤ 2 s** from button‑click to timeline update.

---

## Daily Plan

| Day               | Focus                               | Key Outputs                                                                                               | Guardrails                                   |
| ----------------- | ----------------------------------- | --------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| **15 (Tue 5/20)** | **Kafka Topic**                     | Redpanda service confirmed, topic `gift_events` created via script; health endpoint `/kafka/status`.      | No consumer yet.                             |
| **16 (Wed 5/21)** | **Faust Consumer**                  | `faust_worker.py` consumes `gift_events` and inserts into `vault`. Docker service runs alongside backend. | Manual test with `kcat`.                     |
| **17 (Thu 5/22)** | **Realtime Vault Update**           | Supabase Realtime channel (or 3 s poll) pushes new entry to React timeline instantly.                     | Keep poll fallback; WebSocket optional.      |
| **18 (Fri 5/23)** | **Delete / Edit Endpoints**         | `DELETE /vault/{id}` and `PUT /vault/{id}` with RLS OFF for now; UI buttons + modal.                      | Hard‑confirm dialog before delete.           |
| **19 (Sat 5/24)** | **Symbol Chip UI**                  | Install lucide‑react; render symbol icon + color trail per `symbol_id`. Add filter dropdown.              | Tailwind only—no heavy animation yet.        |
| **20 (Sun 5/25)** | **Dark‑Mode Theme & Mobile Polish** | Extend Tailwind config; toggle dark/light; flex column stacks on phones.                                  | No design rabbit hole—use Tailwind presets.  |
| **21 (Mon 5/26)** | **Retro & Week 4 Setup**            | Retro in `README-W3.md`; seed Week 4 board (Full Corpus ingest).                                          | Optional: embed cron points to 710‑page TSV. |

---

## Stretch Goals

* Push Vault edits via Faust topic for audit trail.
* Use Radix‑UI `Dialog` from shadcn/ui for edit modal.
* Add Supabase Row‑Level Security now that Auth is near.

> **Scope rule:** full‑corpus ingest and advanced symbol animations slide to **Week 4** if they risk Gift latency or stability.
