# Week 6 — Day 39 (Monitoring & Alerts)

> **Target session:** ≈ 2 h  **Goal:** wire up external uptime probes and production alerting so you know within minutes if the API slows down or embeds get pricey. Limit noise to ≤ 3 Slack pings per night.
>
> **Outcome:**
>
> * **UptimeRobot** checks `https://gibsey-api.fly.dev/health` and `https://alpha.gibsey.com` every 5 min.
> * **Grafana Cloud alert rules** fire when P95 latency > 1.8 s or daily cost > \$1.
> * Alerts route to the existing Slack webhook and obey a 15 min alert‑mute window (noise budget).

---

## 1 · UptimeRobot monitors (external)

1. Log in to [https://uptimerobot.com](https://uptimerobot.com) → **Add New Monitor**.
2. **API health**
   \* Type:\* HTTPS
   \* URL:\* `https://gibsey-api.fly.dev/health`
   \* Friendly Name:\* *Gibsey API*
   \* Monitoring Interval:\* 5 minutes
   \* Alert contacts:\* Slack/email.
3. **Front‑end**
   \* URL:\* `https://alpha.gibsey.com`
   Same settings.
4. Copy **“Alert Webhook URL”** (Slack integration) → add to repo secrets:

```bash
gh secret set UPTIME_WEBHOOK --body "https://alert.uptimerobot.com/..."
```

*(Optional: store in Fly secrets too.)*

---

## 2 · Grafana Cloud ingest (token)

1. Create free Grafana Cloud stack → **Log Loki** endpoint URL.
2. Generate **Cloud API/Push token** with `MetricsPublisher` role.
3. Add to repo secrets: `GRAFANA_LOKI_URL`, `GRAFANA_LOKI_TOKEN`.
4. Edit `infra/promtail-config.yaml` (prod overlay):

```yaml
clients:
  - url: $GRAFANA_LOKI_URL
    basic_auth:
      username: ""
      password: $GRAFANA_LOKI_TOKEN
```

Add these as Fly secrets on API app:

```bash
fly secrets set GRAFANA_LOKI_URL=... GRAFANA_LOKI_TOKEN=...
```

Promtail will ship backend JSON logs to Grafana Cloud.

---

## 3 · Alert rules in Grafana

1. Grafana Cloud → **Alerting ▸ Alert rules ▸ New**.
2. **Latency alert**
   *Query (PromQL via Loki metric export):*

   ```promql
   histogram_quantile(0.95,
      sum by(le) (rate(request_duration_seconds_bucket{job="openai_logs"}[5m]))) > 1.8
   ```

   *Condition:* 2 of 3 evaluations true.
   *NoData:* OK.
   *Notifications:* Slack webhook (`SLACK_WEBHOOK_URL`).
   *Mute time interval:* create *night‑mute* 00:00–06:00 local (15 min group wait still applies).
3. **Cost alert**
   *Query*: `sum(rate(cost_usd_total{job="openai_logs"}[1d])) > 1`
   Use same Slack channel.

*(If using hosted Grafana within Fly, create rule files in `infra/grafana/provisioning/alerting/` and commit.)*

---

## 4 · Noise‑budget tuning

* Group by `ruleID` with a 15 min `group_interval` so repeated flaps group into one Slack ping.
  \* Set **“For”** field in each alert rule to *5 minutes* so brief spikes don’t alert.

---

## 5 · Test alerts

1. Temporarily edit API `/health` to return 500 → wait 5 min → UptimeRobot Slack alert fires. Revert change.
2. In Grafana → *Alert rule* → **Test rule** with threshold 0 → confirm Slack ping.
3. Verify only one message per test (mute window working).

---

## 6 · Commit infra docs

Add `docs/monitoring.md`:

```md
# Monitoring & Alerting
* **UptimeRobot:** 5 min checks on API + Front‑end, webhook to Slack.
* **Grafana Cloud:** P95 latency > 1.8 s (5 min) or daily cost > $1.
* Noise budget: group 15 min; mute window 00‑06 local.
```

Commit:

```bash
git checkout -b day39-monitoring
git add infra/promtail-config.yaml docs/monitoring.md
git commit -m "docs/infra: add external uptime & Grafana Cloud alerts"
git push -u origin day39-monitoring
```

PR → **Closes #Day‑39 issue** → merge when checks pass; move card to **Done**.

---

### ✅ End‑of‑Day 39 Definition

* UptimeRobot monitors live; Slack alerts verified.
* Grafana Cloud alert rules active (latency & cost) with grouping + mute.
* Monitoring doc committed.

*Tomorrow (Day 40):* legal placeholder pages and footer links.