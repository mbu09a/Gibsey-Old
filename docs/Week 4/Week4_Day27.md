# Week 4 — Day 27 (Cron Monitor & Alert)

> **Target session:** ≈ 2 h  **Goal:** add a GitHub Actions workflow that watches the nightly **`embed-cron`** run, fails loudly if it exceeds 15 min or exits non‑zero, and posts a Slack alert when cost for the run is > \$0.50 or the job fails.
>
> **Outcome:** Team Slack channel receives a JSON message if embeddings stall or cost spikes; GitHub’s “Cron Monitor” badge shows green for healthy nights.

---

## 1 · Set up Slack webhook secret

1. In Slack workspace → **Apps → Incoming Webhooks** → *Add New Webhook*.
   Choose #gibsey‑alerts, copy Webhook URL.
2. GitHub repo → **Settings → Secrets & variables → Actions → New secret**
   Name: **`SLACK_WEBHOOK_URL`** → paste URL.

---

## 2 · Helper script to summarise last run

Create `scripts/cron_report.py`:

```python
#!/usr/bin/env python3
"""Query the last completed embed-cron run and emit summary JSON."""
import os, sys, json, requests, datetime as dt

repo = os.getenv("GITHUB_REPOSITORY")  # e.g. mbu09a/Gibsey
token = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}

runs = requests.get(f"https://api.github.com/repos/{repo}/actions/workflows/embed-cron.yml/runs?per_page=1", headers=HEADERS).json()["workflow_runs"]
if not runs:
    print("{}")
    sys.exit(0)
run = runs[0]

duration = (dt.datetime.fromisoformat(run["updated_at"].rstrip("Z")) - dt.datetime.fromisoformat(run["created_at"].rstrip("Z"))).total_seconds()/60
status_ok = run["conclusion"] == "success"

# parse cost from run artifacts (optional). Assume job sets output total_cost
jobs = requests.get(run["jobs_url"], headers=HEADERS).json()["jobs"]
cost = 0.0
for step in jobs[0]["steps"]:
    if step.get("name") == "embed":
        outputs = step.get("outputs", {})
        cost = float(outputs.get("total_cost", 0))

summary = {"duration_min": round(duration,1), "status_ok": status_ok, "cost_usd": cost}
print(json.dumps(summary))
if not status_ok or duration > 15 or cost > 0.5:
    print("::set-output name=alert::1")
```

Make executable: `chmod +x scripts/cron_report.py`

---

## 3 · Cron‑monitor workflow

`.github/workflows/cron-monitor.yml`:

```yaml
name: cron-monitor
on:
  schedule:
    - cron: '30 4 * * *'   # run ~30 min after embed-cron finishes
  workflow_dispatch:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run report
        id: rep
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python scripts/cron_report.py > report.json
          cat report.json
          echo "report=$(cat report.json)" >> $GITHUB_OUTPUT
      - name: Slack alert on failure or high cost
        if: steps.rep.outputs.alert == '1'
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
        run: |
          msg=$(cat report.json)
          curl -X POST -H 'Content-type: application/json' --data "{\"text\": \"🔴 Embed cron alert: $msg\"}" $SLACK_WEBHOOK_URL
```

---

## 4 · Expose cost from embed-cron (quick patch)

In `scripts/embed_seed.py` append before exit:

```python
if os.getenv("GITHUB_OUTPUT"):
    with open(os.getenv("GITHUB_OUTPUT"),"a") as f:
        f.write(f"total_cost={usd}\n")
```

In `embed-cron.yml` add after embed step:

```yaml
    outputs:
      total_cost: ${{ steps.embed.outputs.total_cost }}
```

---

## 5 · Badge for README

Add to `README.md`:

```md
![Cron Monitor](https://github.com/mbu09a/Gibsey/actions/workflows/cron-monitor.yml/badge.svg)
```

---

## 6 · Commit & PR

```bash
git checkout -b day27-cron-monitor
git add scripts/cron_report.py scripts/embed_seed.py .github/workflows/cron-monitor.yml README.md
git commit -m "ci: cron monitor with Slack alert on embed failures or cost spike"
git push -u origin day27-cron-monitor
```

Open PR → **Closes #Day-27 issue** → merge when green; card → **Done**.

---

### ✅ End-of-Day 27 Definition

* `cron-monitor` workflow runs daily; Slack alert fires on failure or >\$0.50 cost.
* README badge shows green when last run healthy.

*Tomorrow (Day 28):* Week‑4 retro, Week‑5 board, and optional cost dashboards.