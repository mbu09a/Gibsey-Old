# Week 6 Overview — “Alpha Launch” Sprint (Days 36 – 42)

> **Sprint Goal:** push Gibsey to a public **alpha** at `alpha.gibsey.com`, with automated deployment, uptime monitoring, and basic observability. Collect the first real‑user feedback without breaking the < 2 s SLA.
>
> **Definition of Done**
>
> 1. Front‑end static build and FastAPI API are live on Fly.io (or Render) behind SSL.
> 2. Zero‑downtime GitHub Actions deploy runs on every tagged release (`v0.1.x`).
> 3. Uptime probe, latency alert, and cost alert integrated (Statuspage & Slack).
> 4. Privacy‑policy & TOS stub pages exist and are linked in footer.
> 5. First 25 invited users onboard successfully; feedback issues logged.

---

## Daily Plan

| Day               | Focus                               | Key Outputs                                                                                          | Guardrails                                  |
| ----------------- | ----------------------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| **36 (Tue 6/10)** | **Prod Fly.io Postgres + secrets**  | Fly database provisioned; prod `.env` template; secret upload script.                                | No local traffic yet.                       |
| **37 (Wed 6/11)** | **Backend deploy workflow**         | `deploy-fly.yml` builds & releases API on tag push; health check passes CI.                          | Use `--strategy rolling` to avoid downtime. |
| **38 (Thu 6/12)** | **Static frontend deploy**          | Vite `pnpm build` → Fly static app; CDN caching headers set; env points to prod API URL.             | Verify CORS & cookies.                      |
| **39 (Fri 6/13)** | **Monitoring & alerts**             | UptimeRobot (5 min) + Grafana Cloud alert rule (latency > 1.8 s, cost > \$1/day). Slack integration. | Alert noise budget: max 3/night.            |
| **40 (Sat 6/14)** | **Legal pages & data policy**       | `/privacy`, `/tos`, `/delete-account` request page. Footer links.                                    | No legal review yet—just placeholder copy.  |
| **41 (Sun 6/15)** | **Alpha invite & onboarding guide** | Mail template, Loom walkthrough video, feedback Google Form; send to 25 testers.                     | Limit invite token to 25 sign‑ups.          |
| **42 (Mon 6/16)** | **Retro & Hotfix triage**           | Collect day‑1 feedback, patch critical bugs, write Week‑6 retro.                                     | No new features—bug‑fix only.               |

---

### Stretch Goals

* Blue‑green deploy slots to revert instantly.
* Cloudflare proxy for global edge caching.
* Datadog RUM for front‑end error collection.

> **Scope rule:** Dream/Index modes, full 16‑symbol trails, and mobile PWA stay post‑MVP unless alpha testers block on them.