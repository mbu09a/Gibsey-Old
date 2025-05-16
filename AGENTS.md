# 🤖 Codex Agent Guide for **Gibsey**

Welcome, Codex! This file tells you **how to navigate, build, test, and style** the Gibsey code‑base. Follow these instructions precisely.

---

## 1 · Repository Map

```
/              – mono‑repo root
│
├─ apps/
│   ├─ backend/           # FastAPI  (Python 3.11)
│   └─ frontend/          # React + Vite  (Node 20)
│
├─ db/                    # SQL schema & seed
├─ scripts/               # one‑shot utilities (idempotent)
├─ .devcontainer/         # VS Code / Codespaces config
├─ docker-compose.yml     # dev‑only multi‑service stack
└─ Makefile               # convenience targets
```

---

## 2 · Primary Commands

| Task                   | Command (run from repo root)                          |
| ---------------------- | ----------------------------------------------------- |
| **Start dev stack**    | `make dev` → wraps `docker compose up -d backend db`  |
| **Run backend tests**  | `pytest -q`                                           |
| **Run frontend tests** | `npm test --prefix apps/frontend -- --watchAll=false` |
| **Full lint**          | `make lint` (black, isort, ruff, eslint, prettier)    |
| **One‑shot setup**     | `scripts/setup_dev.sh` → seeds DB & embeddings        |
| **DB reset (tests)**   | `scripts/reset_db.sh`                                 |

> **Codex:** Always execute commands **inside** the `backend` service container (the dev‑container shares the same image).

---

## 3 · Environment Variables

| Name                | Dev Default      | Notes                         |
| ------------------- | ---------------- | ----------------------------- |
| `OPENAI_API_KEY`    | \`\`             | leave blank in CI; mocked     |
| `SUPABASE_URL`      | `http://db:5432` | points to local Postgres      |
| `SUPABASE_ANON_KEY` | \`\`             | dummy in dev / CI             |
| `DEV_MODE`          | `true`           | backend switches to direct DB |

Env‑vars are defined in **`.env.example`**.  CI sets them via the workflow file.

---

## 4 · Docker & Images

* Base images are **pinned**:

  * `python:3.11.4-slim` for backend
  * `node:20.11.1-alpine` for frontend
  * `postgres:15.3` for db
* Images are tagged **immutably** as `ghcr.io/<org>/<service>:<GITHUB_SHA>`.
* Do **not** retag or mutate an existing tag—build a new one.

---

## 5 · Coding Conventions

| Area      | Rule                                                                        |
| --------- | --------------------------------------------------------------------------- |
| Python    | Pydantic v2, type‑hints everywhere, 100‑char lines, Ruff/Black auto‑fix     |
| JS/TS     | React 18 + Vite, TypeScript strict mode, 2‑space indent                     |
| Tests     | Pytest unit tests in `tests/`, frontend tests in `apps/frontend/__tests__/` |
| DB schema | All SQL idempotent (`IF NOT EXISTS`, `CREATE OR REPLACE`)                   |
| Seed data | Use `INSERT … ON CONFLICT DO NOTHING` to avoid duplicates                   |

---

## 6 · Typical Agent Tasks

1. **"Add health‑check endpoint"** → create `GET /health` in FastAPI, add pytest.
2. **"Refactor embedding.py into a class"** → maintain test parity.
3. **"Improve React context: broadcast active Corpus symbol"** → update `SymbolContext.tsx`, write unit test.

Follow the *Primary Commands* table after edits: **lint → tests → make dev**.

---

## 7 · Done?  Submit!

1. `pytest -q` & frontend tests **must** be green.
2. Commit with message `feat: <summary>`.
3. Push branch & open PR. CI will build images, seed DB, and run full test suite.

**Thank you, Codex.** Execute precisely, cite terminal logs in your reply, and request review when complete. 