# Gibsey MVP 🌀

> **A Novel AI OS**

## Overview

**Gibsey** is a multi-layered narrative system that uses AI-generated responses, symbolic embeddings, and dynamic user interaction to deliver a unique reading experience. This repository holds the code for the foundational MVP: a focused, scalable platform enabling readers to:

1. **Read** curated narrative content.
2. **Ask** questions about content.
3. **Receive** AI-driven narrative responses.
4. **Save** these interactions in a personalized **Vault**.

### Week 1 Goal: Walking Skeleton

A minimal, functional stack:

* React (Vite) frontend
* FastAPI backend
* Supabase (Postgres + pgvector)
* OpenAI embeddings & GPT-4o

Full loop: `React → FastAPI → Supabase → React` in ≤ 2 seconds.

---

## Repository Structure

```bash
gibsey/
├── apps
│   ├── frontend # React (Vite + Tailwind)
│   └── backend  # FastAPI + Python 3.11
├── infra
│   └── compose.yaml # Docker Compose setup
├── scripts
│   ├── embed_seed.py # OpenAI embeddings seeder
│   └── build_and_tag.sh # Docker image build & tag script
└── docs
    ├── README-W1.md # Week 1 Overview & Checklist
    └── architecture/
        └── IMAGES.md # Docker image versioning policy
```

---

## Quickstart

### Prerequisites

* Docker & Docker Compose
* Node (≥20), Python (≥3.11)

### Setup & Run

```bash
# Clone & enter repo
git clone <repo_url> && cd gibsey-mvp

# Docker Compose (build & start)
docker compose -f infra/compose.yaml up --build -d
```

Check health:

```bash
curl http://localhost:8000/health
```

Frontend:

```bash
cd apps/frontend && pnpm run dev
# Open http://localhost:5173
```

---

## Daily Workflow (Week 1)

* **Pre-session (5 min)** — read yesterday’s commit; open a new issue.
* **Pomodoro (45 min)** — work in small slices; commit runnable changes.
* **End-session** — push & write 2-sentence progress summary.

---

## Contributing

Use feature branches based on daily tasks (`day1-task-name`) and merge via pull request. CI will lint and verify your changes. Clearly document and test your contributions.

---

## Resources & Documentation

* [Supabase](https://supabase.com/docs)
* [FastAPI](https://fastapi.tiangolo.com/)
* [React + Vite](https://vitejs.dev/guide/)
* [pgvector](https://github.com/pgvector/pgvector)
* [OpenAI API](https://platform.openai.com/docs)

---

## License

MIT License
