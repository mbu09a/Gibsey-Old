# Week 6 — Day 38 (Static Front‑End Deploy on Tag Push)

> **Target session:** ≈ 2 h  **Goal:** build the Vite front‑end for production, deploy it as a Fly.io **static web app** on every version tag (`v*`), and verify CORS + env variables point to the prod API.
>
> **Outcome:** Tagging `v0.1.0-alpha.1` publishes `https://alpha.gibsey.com` (or `gibsey-frontend.fly.dev`) with the latest UI. The site fetches shards from `https://gibsey-api.fly.dev` and auth flows work.

---

## 1 · Create Fly static app

From repo root:

```bash
cd apps/frontend
fly launch --name gibsey-frontend --org personal --no-deploy --region sea --now  # generates fly.toml
```

When prompted, choose **“Static server (Dockerfile not required)”**. Accept defaults, edit created **`fly.toml`** to:

```toml
app = "gibsey-frontend"
primary_region = "sea"
[build]
  builder = "heroku/buildpacks:20"   # tiny Nginx static buildpack
[env]
  VITE_API_BASE = "https://gibsey-api.fly.dev"
  VITE_SUPABASE_URL = "https://xyz.supabase.co"

[[statics]]
  guest_path = "/workspace/dist"
  url_prefix = "/"
```

(*Fly will serve files in `dist/` via Nginx*.)

---

## 2 · Handle CORS & cookies

Ensure backend `fastapi` CORS middleware allows origin `https://gibsey-frontend.fly.dev` and future `alpha.gibsey.com`.

```python
origins = ["http://localhost:5173","https://gibsey-frontend.fly.dev","https://alpha.gibsey.com"]
```

---

## 3 · Add deploy workflow

`.github/workflows/deploy-frontend.yml`:

```yaml
name: deploy-frontend

on:
  push:
    tags: [ 'v*' ]
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
        with: { version: 8 }
      - name: Install deps & build
        working-directory: apps/frontend
        run: |
          pnpm install --frozen-lockfile
          pnpm run build   # output → dist/
      - name: Set up Flyctl
        uses: superfly/flyctl-actions@1.4
      - name: Deploy to Fly
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
        working-directory: apps/frontend
        run: flyctl deploy --remote-only --strategy immediate
      - name: Slack notify
        if: always()
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
        run: |
          curl -X POST -H 'Content-type: application/json' --data "{\"text\": \"Frontend deploy ${{ job.status }} — tag ${{ github.ref_name }}\"}" $SLACK_WEBHOOK_URL
```

No secrets needed besides `FLY_API_TOKEN` & `SLACK_WEBHOOK_URL`.

---

## 4 · Local prod build smoke test

```bash
cd apps/frontend
pnpm run build
npx serve dist  # open http://localhost:3000
```

Open devtools → network calls hit prod API base; auth magic‑link still works (Supabase URL set via env).  Lighthouse Perf should be ≥ 95.

---

## 5 · Domain & SSL note (for Day 40)

Add CNAME `alpha.gibsey.com` → `gibsey-frontend.fly.dev` later; Fly will auto‑issue TLS. Document in alpha checklist.

---

## 6 · Commit & PR

```bash
git checkout -b day38-frontend-deploy
git add apps/frontend/fly.toml .github/workflows/deploy-frontend.yml
# plus any CORS origin additions
git commit -m "ci: auto-deploy static frontend to Fly on version tag"
git push -u origin day38-frontend-deploy
```

Open PR → **Closes #Day-38 issue** → merge once workflow passes on next tag push (`git tag -a v0.1.0-alpha.1 -m "front hotfix" && git push origin v0.1.0-alpha.1`). Move board card to **Done**.

---

### ✅ End-of-Day 38 Definition

* Fly static app `gibsey-frontend` deployed from GitHub Action.
* Vite build outputs served; origin CORS updated.
* Slack notification fires on deploy result.

*Tomorrow (Day 39):* establish monitoring probes and Grafana Cloud alert rules for latency & cost.