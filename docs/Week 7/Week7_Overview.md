# Week 7 Overview — “Post‑MVP Hardening & Quick Wins” Sprint (Days 43 – 49)

> **Sprint Goal:** stabilize the live alpha, deliver the top two user‑requested features (**Vault edit/delete** and **16‑symbol trails**), and prepare for a wider beta wait‑list. Anything bigger than a 1‑day change moves to the new Beta backlog.
>
> **Definition of Done**
>
> 1. Vault entries can be edited or deleted (with undo) and RLS still enforced.
> 2. All 16 Corpus symbols render with color + rotation trails; filter works.
> 3. P90 end‑to‑end latency remains ≤ 2 s after new features.
> 4. Zero Sev‑1 bugs open; Beta wait‑list landing page live.

---

## Daily Plan

| Day               | Focus                            | Key Outputs                                                                           | Guardrails                       |
| ----------------- | -------------------------------- | ------------------------------------------------------------------------------------- | -------------------------------- |
| **43 (Tue 6/17)** | **Bug bash & backlog triage**    | Label all alpha issues Sev‑2/3; write fix plans; close dupes.                         | No feature work today.           |
| **44 (Wed 6/18)** | **Vault edit endpoint & UI**     | `/vault/update` + modal editor; optimistic UI with toast.                             | Keep history record for audit.   |
| **45 (Thu 6/19)** | **Vault delete + undo**          | Soft‑delete flag; 5‑sec snackbar undo; hard purge cron nightly.                       | Ensure RLS on soft‑deleted rows. |
| **46 (Fri 6/20)** | **16‑symbol palette & trails**   | Add SVG trail component; symbol picker shows color ring.                              | No costly animations (GPU safe). |
| **47 (Sat 6/21)** | **Filter logic & latency check** | Top‑bar symbol filter queries Pinecone index by `symbol_id`; update bench script.     | P90 still ≤ 2 s.                 |
| **48 (Sun 6/22)** | **Beta wait‑list page**          | Next‑js landing under `/beta`; collects email → Supabase table; Cloudflare turnstile. | SEO meta tags, no auth required. |
| **49 (Mon 6/23)** | **Week‑7 retro & Beta roadmap**  | Retro doc, burn down Sev‑2 fixes, seed Beta board.                                    | Decide Go/No‑Go on wider launch. |

---

### Stretch Goals

* Social sign‑in (GitHub OAuth) pilot.
* PWA manifest & service‑worker cache.
* Dream/Index early prototype behind `?dream=on` query param.

> **Scope rule:** anything that jeopardizes latency or introduces new data models rolls into the future Beta sprint.