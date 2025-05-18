# Week 5 — Day 35 (Sprint Retro & Alpha‑Launch Checklist)

> **Target session:** 1–2 h  **Goal:** capture Week 5 learnings, run a final smoke test, and prepare an Alpha deployment script (Fly.io or Render) plus a launch-readiness checklist. Mark the project board milestone complete.
>
> **Outcome:** `README‑W5.md` retro committed; `alpha-checklist.md` lists go‑live tasks; Fly.io deploy works from CI; board column archived.

---

## 1 · Write Week 5 retrospective

Create **`docs/README‑W5.md`** (or append):

```md
## Week 5 Retrospective

### Wins 🚀
- Supabase Auth magic‑link operational; RLS locked down Vault.
- Mobile nav & symbol picker performed well (0 layout shifts).
- Lighthouse A11y: **97 mobile / 100 desktop**.
- Grafana dashboard shows accurate daily OpenAI spend.

### Puzzles / friction 🤔
- JWT refresh timing caused 401 loops until retry logic added.
- Safe‑area insets on older Android Chrome inconsistent.

### Scope changes 🔄
- Social sign‑in punted to Post‑MVP.
- PWA offline cache parked for later.

### Metrics 📊 (last 24 h)
| Metric | Value |
|--------|-------|
| Median /ask latency | xxx ms |
| P90 /ask latency | xxx ms |
| Daily OpenAI cost | $0.0xx |

### Team battery 🔋
4/5 – proud of polish; deployment prep next.
```

Commit:

```bash
git add docs/README-W5.md
git commit -m "docs: add Week 5 retrospective"
```

---

## 2 · Draft Alpha launch checklist

Create **`docs/alpha-checklist.md`**:

```md
# Alpha Launch Checklist – Gibsey

## 1. Infrastructure
- [ ] Fly.io Postgres (1 GB RAM) provisioned
- [ ] Fly.io app `gibsey-api` deployed (Dockerfile)
- [ ] Fly.io app `gibsey-frontend` deployed (static build)
- [ ] Pinecone prod index upgraded to Starter‑Plus

## 2. Env vars / Secrets
- [ ] SUPABASE_URL / SERVICE_KEY on backend
- [ ] PINE_API_KEY & ENV
- [ ] OPENAI_API_KEY prod rate‑limit 20 req/min
- [ ] SLACK_WEBHOOK_URL for alerts

## 3. Monitoring
- [ ] UptimeRobot ping `/health` every 5 min
- [ ] Grafana Cloud receiver for Loki shipping
- [ ] OpsGenie alert on embed‑cron failure

## 4. Domain / SSL
- [ ] `alpha.gibsey.com` CNAME → Fly.io front‑end app
- [ ] TLS cert auto‑issued

## 5. Final Smoke Tests
- [ ] Create new user via magic‑link, save Q&A, reload → persists
- [ ] Query heavy shard returns < 2 s
- [ ] Delete entry – RLS prevents other user viewing

## 6. Docs & Comms
- [ ] Update README badge links to prod Grafana
- [ ] Post Alpha invite email to friends list (100 users)
- [ ] Slack channel #alpha‑feedback opened
```

Commit:

```bash
git add docs/alpha-checklist.md
git commit -m "docs: alpha launch checklist"
```

---

## 3 · Add Fly.io deploy GitHub Action (optional)

`.github/workflows/deploy-fly.yml` skeleton:

```yaml
name: deploy-fly
on:
  workflow_dispatch:
  push:
    tags: [ 'v*' ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: superfly/flyctl-actions@1.4
        with:
          args: "deploy --remote-only"
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

Add runbook notes in checklist.

---

## 4 · Update project board

* Mark remaining Week 5 cards **Done**.
* Archive **Week 5 – UX Polish + Auth** column.
* Create **Alpha Launch** milestone if desired.

---

## 5 · Push & PR

```bash
git checkout -b day35-retro-alpha
git push -u origin day35-retro-alpha
```

Open PR → **Closes #Day‑35 issue** → merge when CI green.

---

### ✅ End‑of‑Day 35 Definition

* Week 5 retro committed.
* `alpha-checklist.md` ready; Fly deploy workflow drafted.
* Board closed for Week 5.

**Core 5‑week build complete.** Next stop: tag `v0.1.0‑alpha` and run the checklist! 🚀