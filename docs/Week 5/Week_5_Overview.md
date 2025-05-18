# Week 5 Overview — “UX Polish + Auth” Sprint (Days 29 – 35)

> **Sprint Goal:** add real **Supabase Auth** (email magic‑link) with JWT‑guarded APIs and Row‑Level Security on the Vault, then tighten UX & accessibility for an alpha‑ready feel.
>
> **Definition of Done**
>
> 1. Users can sign‑up / log‑in via modal; session persists via Supabase JS.
> 2. FastAPI validates JWT on protected routes.
> 3. Vault table has RLS policies (owner‑only read/write).
> 4. Mobile nav bar & symbol picker polished; Lighthouse **Accessibility ≥ 95**.
> 5. Grafana dashboard shows token/cost trends fed from JSON logs.

---

## Daily Plan

| Day              | Focus                                 | Key Outputs                                                                                                | Guardrails                            |
| ---------------- | ------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| **29 (Tue 6/3)** | **Auth modal & Supabase session**     | React modal for email magic‑link; Supabase client stores session; `/profile` button shows logged‑in email. | Magic link only—no password UI yet.   |
| **30 (Wed 6/4)** | **JWT guard & RLS policies**          | FastAPI `Depends(auth_user)` verifies JWT; RLS policy on `vault` (`user_id = auth.uid()`).                 | Disable anon key for POST/PUT/DELETE. |
| **31 (Thu 6/5)** | **Magic‑link flow & error states**    | Email templates, resend link, toast errors; “Logged‑out” banner if JWT expired.                            | Rate‑limit resends to 1/min.          |
| **32 (Fri 6/6)** | **Mobile nav & symbol picker polish** | Bottom nav bar on ≤ 640 px; symbol chips selectable via horizontal scroll.                                 | No new pages.                         |
| **33 (Sat 6/7)** | **Accessibility & axe audit**         | Run `@axe-core/react`; fix color contrast, add `aria` labels; Lighthouse A11y ≥ 95.                        | No layout shifts > 0.05.              |
| **34 (Sun 6/8)** | **Grafana cost dashboard**            | Dashboard JSON visualizes daily OpenAI spend; live link in README.                                         | Pull data from JSONL logs for now.    |
| **35 (Mon 6/9)** | **Retro & Alpha checklist**           | Week‑5 retro; Alpha launch checklist (Fly.io deploy script, uptime monitor).                               | Skip deploy if blockers found.        |

---

### Stretch Goals

* Social sign‑in (GitHub OAuth) via Supabase.
* Offline‑first PWA install prompt.
* Voice‑over TTS toggle for answers.

> **Scope rule:** any Dream/Index modes still belong to **Post‑MVP**; don’t touch until after alpha launch.