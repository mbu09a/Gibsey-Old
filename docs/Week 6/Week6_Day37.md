# Week 6 — Day 37 (API Auto‑Deploy on Tag Push)

> **Target session:** ≈ 2 h  **Goal:** set up a GitHub Actions workflow that builds and deploys the **gibsey-api** Fly.io app whenever a Git tag matching `v*` is pushed (or on manual dispatch). Include post‑deploy health check and Slack notification.
>
> **Outcome:** Tagging `v0.1.0-alpha` pushes a green CI run that ends with “🚀 Deployment succeeded”, and `curl https://gibsey-api.fly.dev/health` returns `{status:"ok"}`.

---

## 1 · Fly deploy workflow

Create **`.github/workflows/deploy-api.yml`**:

```yaml
name: deploy-api

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Flyctl
        uses: superfly/flyctl-actions@1.4
        with:
          version: latest

      - name: Deploy API to Fly (rolling)
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
        working-directory: apps/backend
        run: |
          flyctl deploy --remote-only --strategy rolling --build-arg GIT_SHA=${{ github.sha }}

      - name: Health check
        run: |
          for i in {1..5}; do
            sleep 5
            STATUS=$(curl -s https://gibsey-api.fly.dev/health | jq -r .status || true)
            if [ "$STATUS" = "ok" ]; then echo "API healthy" && exit 0; fi
            echo "Health check attempt $i failed";
          done
          echo "Health check failed" && exit 1

      - name: Slack notify
        if: always()
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
        run: |
          STATUS="${{ job.status }}"
          curl -X POST -H 'Content-type: application/json' --data "{\"text\": \"API deploy $STATUS — tag ${{ github.ref_name }}\"}" $SLACK_WEBHOOK_URL
```

**Secrets required** (in repo → *Settings ▸ Secrets*):

* `FLY_API_TOKEN` – create via `fly auth token` on local machine.
* `SLACK_WEBHOOK_URL` – existing from Day 27.

---

## 2 · Update backend Dockerfile for build arg (optional)

In `apps/backend/Dockerfile` add:

```dockerfile
ARG GIT_SHA=local
LABEL git_sha=$GIT_SHA
```

Fly UI will now show image label.

---

## 3 · Bump version & push tag

```bash
git tag -a v0.1.0-alpha -m "Alpha deploy"
git push origin v0.1.0-alpha
```

Watch *Actions* tab → **deploy-api** workflow runs. After success:

```bash
curl https://gibsey-api.fly.dev/health
```

Expect `{"status":"ok","env":"prod"}`.

---

## 4 · README badge (optional)

Add under CI badges:

```md
[![Deploy API](https://github.com/mbu09a/Gibsey/actions/workflows/deploy-api.yml/badge.svg)](https://github.com/mbu09a/Gibsey/actions/workflows/deploy-api.yml)
```

Commit badge separately if desired.

---

## 5 · Commit & PR

```bash
git checkout -b day37-api-deploy
git add .github/workflows/deploy-api.yml apps/backend/Dockerfile README.md
git commit -m "ci: auto‑deploy API to Fly on version tag"
git push -u origin day37-api-deploy
```

PR → **Closes #Day-37 issue** → merge when workflow passes (tag deploy already tested). Move board card to **Done**.

---

### ✅ End‑of‑Day 37 Definition

* `deploy-api.yml` exists and succeeds on tag push.
* Post‑deploy health check green; Slack message posts.
* Badge (optional) shows latest workflow status.

*Tomorrow (Day 38):* set up static front‑end build & deploy workflow on tag push.