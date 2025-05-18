# Week 5 — Day 34 (Grafana Cost & Token Dashboard)

> **Target session:** ≈ 2 h  **Goal:** visualize daily OpenAI spend and token usage in Grafana, using the JSONL logs already written by the metrics decorator (Day 12). Provision the dashboard automatically so it appears on container startup.
>
> **Outcome:** Visiting `http://localhost:3000` shows a **Gibsey – Cost** dashboard with two panels: *Daily USD Cost* and *Daily Prompt/Completion Tokens*. The dashboard JSON lives in the repo and loads via Grafana provisioning.

---

## 1 · Add Grafana & Loki to docker‑compose

Edit **`infra/compose.yaml`** and append:

```yaml
  loki:
    image: grafana/loki:2.9.6
    command: -config.file=/etc/loki/local-config.yaml
    ports: ["3100:3100"]

  promtail:
    image: grafana/promtail:2.9.6
    volumes:
      - ../logs:/var/log/gibsey:ro
      - ./promtail-config.yaml:/etc/promtail/config.yaml
    command: -config.file=/etc/promtail/config.yaml

  grafana:
    image: grafana/grafana:10.4.0
    ports: ["3000:3000"]
    volumes:
      - ../infra/grafana/provisioning:/etc/grafana/provisioning
      - ../infra/grafana/dashboards:/var/lib/grafana/dashboards
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    depends_on: [loki]
```

Create `infra/promtail-config.yaml`:

```yaml
server:
  http_listen_port: 9080
positions:
  filename: /tmp/positions.yaml
clients:
  - url: http://loki:3100/loki/api/v1/push
scrape_configs:
  - job_name: gibsey_logs
    static_configs:
      - targets: [localhost]
        labels:
          job: openai_logs
          __path__: /var/log/gibsey/openai-*.jsonl
```

---

## 2 · Provision Grafana data source & dashboard

`infra/grafana/provisioning/datasources/loki.yml`:

```yaml
apiVersion: 1
datasources:
  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
    isDefault: true
```

Create folder `infra/grafana/dashboards/` and dashboard provisioning file `provisioning/dashboards/all.yml`:

```yaml
apiVersion: 1
datasources:
- name: Loki
  orgId: 1
providers:
  - name: local-dashboards
    orgId: 1
    folder: Gibsey
    type: file
    options:
      path: /var/lib/grafana/dashboards
```

---

## 3 · Build dashboard JSON

### 3.1 Open Grafana locally

```bash
docker compose -f infra/compose.yaml up -d loki promtail grafana
open http://localhost:3000  # admin / admin
```

Add new dashboard → Panel 1 (Daily USD Cost):

```logql
sum by (day) (sum_over_time(
  {job="openai_logs"} | json cost_usd="cost_usd" | unwrap cost_usd
  [1d])
)
```

Set *Legend* = `{{day}}`, *unit* = currency USD.
Panel 2 (Prompt vs Completion Tokens):

```logql
sum by (kind, day) (sum_over_time(
  {job="openai_logs"} | json prompt_tokens="prompt_tokens", completion_tokens="completion_tokens" |
  line_format "{kind="prompt"} {prompt_tokens}" {kind="completion"} {completion_tokens} |
  unwrap prompt_tokens as tokens kind="prompt" |
  unwrap completion_tokens as tokens kind="completion"
  [1d]))
```

Save dashboard as **Gibsey – Cost** in *Gibsey* folder.

### 3.2 Export JSON

Dashboard settings → JSON model → Copy → save to `infra/grafana/dashboards/cost.json`.

---

## 4 · Re‑run stack to auto‑load dashboard

```bash
docker compose -f infra/compose.yaml up -d --build
```

Visit Grafana again → **Dashboards ▸ Gibsey ▸ Cost** should load without manual import.

---

## 5 · README badge & link

Add to main `README.md`:

```md
[![Grafana](https://img.shields.io/badge/Grafana-dashboard-orange)](http://localhost:3000/d/Gibsey-Cost)
```

---

## 6 · Commit & PR

```bash
git checkout -b day34-grafana-cost
git add infra/compose.yaml infra/promtail-config.yaml infra/grafana
git add README.md
git commit -m "feat: Grafana+Loki stack and cost/token dashboard"
git push -u origin day34-grafana-cost
```

Open PR → **Closes #Day-34 issue** → merge when CI passes; move card to **Done**.

---

### ✅ End-of-Day 34 Definition

* Loki + Promtail shipping JSONL costs to Grafana.
* Dashboard auto‑loads via provisioning; shows daily USD & token metrics.
* README badge links to Cost dashboard (local URL for now).

*Tomorrow (Day 35):* Week‑5 retro and alpha‑launch readiness checklist.