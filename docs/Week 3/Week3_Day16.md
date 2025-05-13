# Week 3 — Day 16 (Faust Consumer → Persist Gifts)

> **Target session:** ≈ 3 h  **Goal:** publish a `gift_events` message whenever something is saved to the Vault and have a Faust worker consume that topic, inserting the row into the database. Manual calls to `/vault/save` should show up in the timeline **without** direct DB writes from the API.
>
> **Outcome:** FastAPI publishes; Faust consumer persists; timeline updates as before but now through the event spine.

---

## 1 · Add Faust & publisher code

\### 1.1 Update backend dependencies
Append to `apps/backend/requirements.txt`:

```
faust-streaming==0.10.22
aiokafka>=0.10
```

Re‑build backend image later.

\### 1.2 Publish to `gift_events` inside `/vault/save`
In `app/main.py` (or a new `events.py`):

```python
import json, asyncio
from aiokafka import AIOKafkaProducer

producer: AIOKafkaProducer | None = None

async def get_producer():
    global producer
    if producer is None:
        producer = AIOKafkaProducer(bootstrap_servers="kafka:9092")
        await producer.start()
    return producer

async def publish_gift(payload: dict):
    prod = await get_producer()
    await prod.send_and_wait("gift_events", json.dumps(payload).encode())
```

In `/vault/save`, **replace** the direct DB insert with an async publish:

```python
@app.post("/vault/save", status_code=202)
async def save_to_vault(req: VaultSaveRequest):
    payload = req.model_dump() | {"ts": time.time()}
    await publish_gift(payload)
    return {"queued": True}
```

*(Keep the old DB insert code commented for fallback.)*

---

## 2 · Faust worker service

\### 2.1 Faust app definition (`apps/worker/worker.py`)

```python
import faust, os, time
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
assert SUPABASE_URL and SUPABASE_KEY, "Set Supabase envs in worker"

sb = create_client(SUPABASE_URL, SUPABASE_KEY)
app = faust.App(
    "gibsey-gift-worker",
    broker="kafka://kafka:9092",
    value_serializer="raw",
)

gifts_topic = app.topic("gift_events")

@app.agent(gifts_topic)
async def persist(stream):
    async for raw in stream:
        payload = app.serializer.loads(raw)
        sb.table("vault").insert(payload).execute()
        print("[faust] persisted gift", payload["question"][:40])
```

\### 2.2 Worker Dockerfile
Create `apps/worker/Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /code
COPY ./worker.py .
RUN pip install faust-streaming supabase==2.0.0 aiokafka
ENTRYPOINT ["python", "worker.py"]
```

\### 2.3 Add service to `infra/compose.yaml`

```yaml
  faust-worker:
    build: ../apps/worker
    depends_on: [kafka]
    env_file:
      - ../.env
```

---

## 3 · Re‑build & up stack

```bash
docker compose -f infra/compose.yaml build faust-worker backend
docker compose -f infra/compose.yaml up -d kafka kafka-init faust-worker backend
```

Run `docker compose logs -f faust-worker` in another terminal—should show “connected” messages.

---

## 4 · Manual E2E test

1. **Publish:**

```bash
curl -X POST http://localhost:8000/vault/save \
  -H 'Content-Type: application/json' \
  -d '{"page_id":1,"question":"TEST Q?","answer":"TEST A"}'
```

Should return `{ "queued": true }`.

2. **Observe worker log** → should print `persisted gift TEST Q` within < 1 s.

3. **Verify timeline** ([http://localhost:5173](http://localhost:5173)) refreshes or auto‑updates to show the entry.

---

## 5 · CI (skip worker build)

Add new service build to CI workflow only for Docker build step; unit tests unchanged.

---

## 6 · Commit & PR

```bash
git checkout -b day16-faust-consumer
git add apps/worker infra apps/backend/app events code changes
git commit -m "feat: Faust consumer persists gift_events to Vault; /vault/save now publishes"
git push -u origin day16-faust-consumer
```

Open PR → **Closes #Day-16 issue** → merge after green.
Move board card to **Done**.

---

### ✅ End-of-Day 16 Definition

* `/vault/save` no longer writes DB directly; publishes to topic.
* Faust worker consumes `gift_events` and inserts into `vault` table.
* Manual test shows end-to-end path < 2 s.

*Tomorrow (Day 17):* wire Supabase Realtime (or poll) so timeline updates without page refresh.
