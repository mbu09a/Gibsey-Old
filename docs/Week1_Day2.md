# Week 1 — Day 2 (Backend Bootstrap)

> **Target session:** 2–3 h
>
> **Goal:** a FastAPI service that answers `GET /health → {"status":"ok"}` and runs inside Docker Compose with environment variables loaded from `.env`.

---

## 1. Create the FastAPI app

```bash
cd apps/backend
mkdir app && touch app/__init__.py app/main.py app/config.py
```

### `app/config.py`

```python
from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
    env: str = "local"
    project_name: str = "Gibsey MVP"

    class Config:
        env_file = ".env"
        extra = "ignore"

@lru_cache
def get_settings() -> Settings:  # dependency‑friendly
    return Settings()
```

### `app/main.py`

```python
from fastapi import Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware
from .config import Settings, get_settings

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health(settings: Settings = Depends(get_settings)):
    return {"status": "ok", "env": settings.env}
```

---

## 2. Update dependencies

Append to `requirements.txt`:

```
pydantic[dotenv]
python-multipart   # future‑proof uploads
```

Re‑build:

```bash
cd ../../..
docker compose -f infra/compose.yaml build backend
```

---

## 3. Wire env vars in Compose

Edit `infra/compose.yaml` backend service:

```yaml
    env_file:
      - ../.env
```

*(Commit the `.env.example` earlier—never the real `.env`.)*

---

## 4. Manual smoke test

```bash
docker compose -f infra/compose.yaml up -d
curl http://localhost:8000/health  # → {"status":"ok","env":"local"}
docker compose down
```

If it times out, run `docker compose logs backend` to debug.

---

## 5. Unit‑test placeholder (optional but fast)

```bash
pip install pytest  # local only
mkdir -p apps/backend/tests
cat > apps/backend/tests/test_health.py <<'PY'
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"
PY
```

Run locally:

```bash
pytest -q apps/backend/tests
```

*(Add `pytest` to `requirements.txt` if you’ll wire it in CI today; else defer.)*

---

## 6. Update CI (quick win)

In `.github/workflows/ci.yml`, under **backend-lint** job add:

```yaml
      - name: test
        run: |
          pip install pytest
          pytest -q app || true  # don’t fail pipeline yet
```

Commit & push:

```bash
git add apps/backend app/ infra/compose.yaml .github/workflows/ci.yml
git commit -m "feat: FastAPI /health route + env config"
git push --set-upstream origin day2-backend-bootstrap
```

Open PR → link to *Day 2* issue → merge after green check.

---

## 7. Move board card to *Done* & journal

*Close “Day 2 – FastAPI health route” issue.* In its comment box write a two‑sentence note:

> “/health live in Docker, CI green. No blockers; hit 90 min.”

---

### ✅ End‑of‑Day 2 Definition

* Docker‑compose boots backend + db.
* `curl localhost:8000/health` responds.
* CI shows at least lint + stub test.

*Tomorrow*: Supabase pages table + seed one shard.
