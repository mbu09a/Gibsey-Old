# Week 6 — Day 36 (Provision Fly.io Postgres & Prod Secrets)

> **Target session:** ≈ 2 h  **Goal:** spin up a managed Fly.io Postgres cluster for production, capture the credentials in a secured `.env.prod` template, and store them as secrets in both the **API** and **Frontend** Fly apps.
>
> **Outcome:** A **`gibsey-db`** Postgres instance is live in the same region as your API app; `fly secrets set …` has populated all required variables; local prod builds can source `.env.prod`.

---

## 1 · Install & log in to Fly.io

```bash
brew install flyctl   # macOS — adjust for other OS
fly auth login        # opens browser for GitHub OAuth
```

Ensure you’re on the correct Fly org: `fly orgs list` → note slug (e.g., `personal`).

---

## 2 · Create Postgres cluster

```bash
fly pg create --name gibsey-db --org personal --region sea --vm-size shared-cpu-1x --volume-size 10
```

*Pick the same region as your future API app (`sea` = Seattle). 10 GB is enough for alpha.*
The CLI returns:

```
Postgres cluster gibsey-db created
  HOST: gibsey-db.internal
  ROLE: primary
  USER: postgres
  PASSWORD: <generated>
  DATABASE: postgres
```

Copy **HOST**, **PASSWORD**. Create a service role user for Supabase access:

```bash
fly pg connect -a gibsey-db
CREATE USER gibsey_app PASSWORD 'REPLACE_ME';
CREATE DATABASE gibsey OWNER gibsey_app;
\q
```

---

## 3 · Update `.env.prod.example`

Create a new template file in repo root:

```env
# ─── DATABASE ────────────────────────────────────────────────
DATABASE_URL=postgresql://gibsey_app:REPLACE_PASSWORD@gibsey-db.internal:5432/gibsey
DB_SCHEMA=public

# ─── SUPABASE SERVICE KEYS (prod project) ───────────────────
SUPABASE_URL=https://xyz.supabase.co
SUPABASE_SERVICE_KEY=xxxxxxxxx
SUPABASE_JWT_SECRET=xxxxxxxxx

# ─── PINECONE / OPENAI / SLACK same as dev but prod values ──
PINE_ENV=gcp-starter
PINE_API_KEY=xxxxx
OPENAI_API_KEY=xxxxx
SLACK_WEBHOOK_URL=xxxxx
```

Commit the **example** file, **never** the real `.env.prod`.

---

## 4 · Store Fly secrets

### 4.1 API app secrets

Assuming you created Fly app `gibsey-api` earlier (if not: `fly launch` in `apps/backend`):

```bash
cd apps/backend
fly secrets set DATABASE_URL="postgresql://gibsey_app:..." \
               SUPABASE_URL="https://xyz.supabase.co" \
               SUPABASE_SERVICE_KEY="..." \
               SUPABASE_JWT_SECRET="..." \
               PINE_API_KEY="..." \
               OPENAI_API_KEY="..." \
               SLACK_WEBHOOK_URL="..."
```

### 4.2 Front‑end app secrets (only public URL)

```bash
cd ../../apps/frontend
fly secrets set VITE_SUPABASE_URL="https://xyz.supabase.co" \
               VITE_API_BASE="https://gibsey-api.fly.dev"
```

*(Frontend doesn’t need service keys.)*

---

## 5 · Local prod run test

Export vars from `.env.prod` and run migrations:

```bash
source .env.prod
alembic upgrade head   # or your FastAPI migration cmd
uvicorn app.main:app --port 8000 --reload  # point DATABASE_URL to Fly internal FQDN; works via WireGuard
```

If connection fails, install **Fly WireGuard** (`fly wireguard create`) so `*.internal` DNS resolves.

---

## 6 · Add `fly.toml` files to repo (versioned)

`apps/backend/fly.toml` minimal example:

```toml
app = "gibsey-api"
primary_region = "sea"
[build]
  dockerfile = "Dockerfile"
[env]
  PORT = "8080"
[deploy]
  strategy = "rolling"
```

Similar for `apps/frontend` static deploy.
Commit:

```bash
git checkout -b day36-fly-postgres
git add .env.prod.example apps/*/fly.toml infra/
git commit -m "chore: provision Fly Postgres and prod env templates"
git push -u origin day36-fly-postgres
```

PR → **Closes #Day-36 issue** → merge once CI passes (backend tests should still hit dev DB).
Move board card to **Done**.

---

### ✅ End-of-Day 36 Definition

* Fly Postgres `gibsey-db` running, credentials stored as secrets.
* `.env.prod.example` committed for future deploy docs.
* Local prod env connects via WireGuard.

*Tomorrow (Day 37):* implement GitHub Action to auto‑deploy API on new tags.