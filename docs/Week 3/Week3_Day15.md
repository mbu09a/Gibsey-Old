# Week 3 — Day 15 (Redpanda Topic + Health Endpoint)

> **Target session:** ≈ 2 h  **Goal:** stand up Redpanda inside Docker Compose, create the `gift_events` topic, and expose a simple `/kafka/status` endpoint so the frontend can display broker health.
>
> **Outcome:** `docker compose up` shows a healthy Kafka broker, `curl /kafka/status` returns `{ "brokers": 1, "topic": "gift_events", "ok": true }`.

---

## 1 · Add Redpanda to `infra/compose.yaml`

```yaml
  kafka:
    image: redpanda/redpanda:v24.1.2
    command: >-
      redpanda start
      --overprovisioned
      --smp 1
      --memory 256M
      --reserve-memory 0M
      --node-id 0
      --check=false
    ports:
      - "9092:9092"        # Kafka API
      - "9644:9644"        # Admin HTTP (optional)
```

Commit:

```bash
git add infra/compose.yaml
```

---

## 2 · Create a tiny topic‑init script

Place in `scripts/kafka_bootstrap.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
TOPIC="gift_events"

rpk cluster info --brokers localhost:9092 >/dev/null 2>&1 || {
  echo "Redpanda not up; skipping topic bootstrap" && exit 1
}

echo "Ensuring topic $TOPIC exists…"
if ! rpk topic list | grep -q "$TOPIC"; then
  rpk topic create "$TOPIC" -p 1 -r 1
  echo "Created $TOPIC"
else
  echo "$TOPIC already exists"
fi
```

Add helper image to Compose so the script can use **`rpk`**:

```yaml
  kafka-init:
    image: redpanda/redpanda:v24.1.2
    depends_on: [kafka]
    entrypoint: ["/bin/bash", "/code/scripts/kafka_bootstrap.sh"]
    volumes:
      - ../scripts:/code/scripts
```

*(Container exits immediately after topic creation.)*
Make script executable:

```bash
chmod +x scripts/kafka_bootstrap.sh
```

Commit:

```bash
git add scripts/kafka_bootstrap.sh infra/compose.yaml
```

---

## 3 · Add health endpoint to FastAPI

In `apps/backend/app/main.py`:

```python
from aiokafka import AIOKafkaAdminClient

@app.get("/kafka/status")
async def kafka_status():
    admin = AIOKafkaAdminClient(bootstrap_servers="kafka:9092")
    try:
        await admin.start()
        topics = await admin.list_topics()
        ok = "gift_events" in topics
        return {"brokers": len(admin._client.cluster.brokers()), "topic": "gift_events", "ok": ok}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
    finally:
        await admin.close()
```

Add dep to `requirements.txt`:

```
aiokafka>=0.10
```

Re‑build backend:

```bash
docker compose -f infra/compose.yaml build backend && docker compose up -d
```

---

## 4 · Smoke test topic & endpoint

```bash
docker compose -f infra/compose.yaml up -d kafka kafka-init backend
curl localhost:8000/kafka/status | jq .
```

Expected:

```json
{ "brokers": 1, "topic": "gift_events", "ok": true }
```

Optional manual check:

```bash
docker exec -it $(docker ps -qf name=kafka) rpk topic list
```

---

## 5 · Commit & PR

```bash
git checkout -b day15-kafka-topic
git add apps/backend app/ infra/ scripts/
git commit -m "feat: Redpanda service, gift_events topic bootstrap, /kafka/status endpoint"
git push -u origin day15-kafka-topic
```

Open PR → **Closes #Day‑15 issue** → merge when CI green.
Move board card to **Done**.

---

### ✅ End‑of‑Day 15 Definition

* Redpanda broker container running via Compose.
* `gift_events` topic auto‑created by bootstrap script.
* `/kafka/status` endpoint returns `{ ok: true }`.

*Tomorrow (Day 16):* implement Faust consumer that ingests `gift_events` and persists to Vault.
