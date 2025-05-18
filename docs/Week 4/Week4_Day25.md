# Week 4 — Day 25 (Latency Benchmark & CI Gate)

> **Target session:** ≈ 2 h  **Goal:** build a script that fires a batch of random `/ask` queries and records latency, token counts, and cost; fail CI if P90 latency exceeds **1.5 s**. Provide a lightweight CSV report for analysis.
>
> **Outcome:** `scripts/bench.py` outputs a CSV + console summary; GitHub Action `bench-check.yml` runs it on PRs and blocks merges when latency regresses.

---

## 1 · Create benchmark script

`scripts/bench.py`:

```python
#!/usr/bin/env python3
"""Latency benchmark for /ask.
Usage: python bench.py --n 50 --pinecone
"""
import argparse, csv, json, os, random, statistics, time, datetime as dt
import requests

API = os.getenv("API_BASE", "http://localhost:8000")
QUESTIONS = [
    "What is the hidden theme of this shard?",
    "Who is the narrator speaking to?",
    "Explain the symbol in one sentence?",
    "How does this shard connect to fate?",
    "Summarize in 10 words?",
]

def run_batch(n: int):
    rows = []
    for i in range(n):
        q = random.choice(QUESTIONS)
        t0 = time.perf_counter()
        r = requests.post(f"{API}/ask", json={"page_id": 1, "question": q})
        latency = (time.perf_counter()-t0)*1000
        headers = r.headers
        rows.append({
            "ts": dt.datetime.utcnow().isoformat()+"Z",
            "lat_ms": latency,
            "prompt_tok": headers.get("X-Prompt-Tokens",0),
            "comp_tok": headers.get("X-Completion-Tokens",0),
            "usd": headers.get("X-Cost-USD",0),
        })
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20)
    args = ap.parse_args()
    rows = run_batch(args.n)
    p90 = statistics.quantiles([r["lat_ms"] for r in rows], n=100)[89]
    print(f"P90 latency: {p90:.0f} ms (target ≤ 1500)")
    csv_file = f"bench-{dt.date.today()}.csv"
    with open(csv_file,"w",newline="") as f:
        w = csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    print("wrote", csv_file)
    # exit 1 if too slow
    if p90 > 1500:
        print("FAIL: latency regression")
        exit(1)

if __name__ == "__main__":
    main()
```

Make executable: `chmod +x scripts/bench.py`

---

## 2 · Add CI workflow

`.github/workflows/bench-check.yml`:

```yaml
name: latency-bench
on:
  pull_request:
    paths: [ 'apps/backend/**', 'apps/frontend/**', 'scripts/**' ]

jobs:
  bench:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: supabase/postgres:15
        ports: [ '5432:5432' ]
      kafka:
        image: redpanda/redpanda:v24.1.2
        ports: [ '9092:9092' ]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - uses: pnpm/action-setup@v3
        with: { version: 8 }
      - name: Install deps
        run: |
          pip install -r apps/backend/requirements.txt
      - name: Start backend (minimal)
        run: |
          uvicorn apps.backend.app.main:app --port 8000 &
          sleep 10
      - name: Run benchmark
        env:
          API_BASE: http://localhost:8000
        run: python scripts/bench.py --n 20
```

*(The service block is a fast placeholder; adjust if your backend needs Kafka.)*

---

\## 3 · Local dry‑run

```bash
python scripts/bench.py --n 10
```

Confirm CSV written and P90 printed.

---

## 4 · Git ignore reports (optional)

```bash
echo "bench-*.csv" >> .gitignore
```

---

## 5 · Commit & PR

```bash
git checkout -b day25-bench
git add scripts/bench.py .github/workflows/bench-check.yml .gitignore
git commit -m "ci: latency benchmark script & gate (P90 ≤ 1.5 s)"
git push -u origin day25-bench
```

Open PR → **Closes #Day‑25 issue** → CI should run bench job; merge if green.
Move card to **Done**.

---

### ✅ End‑of‑Day 25 Definition

* `scripts/bench.py` outputs CSV & enforces P90 ≤ 1.5 s.
* GitHub Actions job fails PR when latency regresses.

*Tomorrow (Day 26):* loading skeleton component and “Load more” paging in search results.