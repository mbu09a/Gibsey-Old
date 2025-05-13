# Week 1 — Day 1 (Repo & CI Skeleton)

> **Target session time:** 2–3 h after work
>
> **Goal:** A monorepo that can `docker compose up`, passes a trivial CI check, and gives you instant feedback for future PRs. *Nothing more.*

---

## 1. Confirm local pre‑reqs

* **Docker Desktop** running (test with `docker ps`).
* **Node ≥ 20 / npm ≥ 10** (`node -v`).
* **Python 3.11** (`python --version`).

If any are missing → install before continuing.

---

## 2. Flesh out repo layout

Inside the root of `gibsey-mvp` (Week 1 branch):

```bash
# Back end
mkdir -p apps/backend/{app,tests}

# Front end
mkdir -p apps/frontend/src

# Infrastructure
mkdir -p infra
```

### `.gitignore` (root)

Add/append:

```
.env
__pycache__/
node_modules/
.DS_Store
*.pyc
```

Commit:

```bash
git add .gitignore apps
git commit -m "chore: scaffold backend/frontend dirs"
```

---

## 3. Docker Compose (minimal)

Create `infra/compose.yaml`:

```yaml
name: gibsey-dev-stack
services:
  backend:
    build: ../apps/backend
    command: ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    volumes:
      - ../apps/backend:/code
    ports: ["8000:8000"]

  db:
    image: supabase/postgres:15
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: gibsey
    ports: ["5432:5432"]
```

*(Frontend container lands Day 5.)*

Build context `apps/backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /code
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

`apps/backend/requirements.txt` (temporary):

```
fastapi
uvicorn[standard]
python-dotenv
```

Commit:

```bash
git add infra apps/backend/Dockerfile apps/backend/requirements.txt
git commit -m "infra: minimal docker compose for backend + db"
```

Test:

```bash
docker compose -f infra/compose.yaml up --build -d
curl http://localhost:8000/health || echo "(expected 404 – route lands Day 2)"
docker compose down
```

---

## 4. GitHub Actions – real checks

Replace placeholder `ci.yml` with:

```yaml
name: CI
on: [push, pull_request]
jobs:
  backend-lint:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: apps/backend
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install ruff==0.4.1
      - run: ruff --output-format=github . || true  # allow warnings for now
  frontend-lint:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: apps/frontend
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: echo "TODO: add eslint when frontend bootstrapped"
```

Commit & push:

```bash
git add .github/workflows/ci.yml
git commit -m "ci: backend lint via Ruff, frontend placeholder"
git push
```

Verify **CI passes** in GitHub → Actions.

---

## 5. Open Day‑1 PR & self‑review

```bash
git checkout -b day1-skeleton
# push branch
```

Create Pull Request → link to *Day 1* issue → self‑review → merge.

Move **“Day 1 – Repo & CI skeleton”** card to *Done*.

---

### ✨ End-of-Day 1 checklist

* [ ] `infra/compose.yaml` builds backend+db without error.
* [ ] CI workflow starts and shows green check.
* [ ] Day‑1 PR merged into `week1`.

> **Congratulations** – tomorrow you’ll write your first FastAPI route, but tonight’s foundation makes every future diff visible and reproducible.
