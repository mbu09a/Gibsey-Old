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
* PostgreSQL with pgvector
* OpenAI embeddings & GPT-4o

Full loop: `React → FastAPI → PostgreSQL → React` in ≤ 2 seconds.

---

## Repository Structure

```bash
gibsey/
├── apps
│   ├── frontend # React (Vite + Tailwind)
│   └── backend  # FastAPI + Python 3.11
├── db
│   └── init.sql     # Database schema and initialization
├── scripts
│   ├── setup_dev.sh # Development environment setup
│   ├── reset_db.sh  # Database reset for testing
│   └── embed_seed.py # OpenAI embeddings seeder
├── tests            # Test suite
├── docker-compose.yml # Local development stack
└── docs
    ├── README-W1.md # Week 1 Overview & Checklist
    └── architecture/
        └── IMAGES.md # Docker image versioning policy
```

---

## Quickstart

### Prerequisites

* Docker & Docker Compose
* Python 3.11+
* Node.js 18+ (for frontend development)

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/gibsey.git
   cd gibsey
   ```

2. **Set up the development environment**
   ```bash
   # Start the database
   docker compose up -d db
   
   # Run the setup script
   ./scripts/setup_dev.sh
   ```

3. **Install Python dependencies**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-test.txt
   ```

4. **Start the development servers**
   ```bash
   # Backend (in one terminal)
   cd apps/backend && uvicorn main:app --reload
   
   # Frontend (in another terminal)
   cd apps/frontend && npm install && npm run dev
   ```

   The application should now be available at http://localhost:5173

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=.

# Reset the test database
./scripts/reset_db.sh
```

### Database Management

- **Initialize database**: `docker compose up -d db`
- **Run migrations**: `psql -h localhost -U postgres -d gibsey -f db/init.sql`
- **Reset database**: `./scripts/reset_db.sh`

### Daily Workflow

* **Pre-session (5 min)** — review previous work and plan tasks
* **Work session (45 min)** — implement features in small, testable chunks
* **End-session** — commit changes and document progress

---

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes and write tests
3. Run tests: `pytest`
4. Commit your changes: `git commit -m "Add your feature"`
5. Push to the branch: `git push origin feature/your-feature`
6. Open a pull request

---

## Resources & Documentation

* [FastAPI](https://fastapi.tiangolo.com/)
* [React + Vite](https://vitejs.dev/guide/)
* [PostgreSQL](https://www.postgresql.org/docs/)
* [pgvector](https://github.com/pgvector/pgvector)
* [OpenAI API](https://platform.openai.com/docs)

---

## License

MIT License
