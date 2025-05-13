# Week 2 — Day 12 (Latency & Cost Instrumentation)

> **Target session:** 1 h (light)  **Goal:** make every OpenAI call self‑logging: emit timing, token usage, and cost to both stdout **and** a JSONL file under `logs/`. Add a reusable decorator so future agents inherit instrumentation automatically.
>
> **Outcome:** Each `/ask` request writes one JSON line containing timing + cost, and response headers expose the same data for the frontend console.

---

## 1 · Create reusable decorator

Create `apps/backend/app/metrics.py`:

```python
from __future__ import annotations
import functools, json, pathlib, time, datetime as dt
from typing import Callable, Any

# current OpenAI pricing (USD per 1k tokens — adjust as needed)
PRICE = {
    "text-embedding-3-small": {"prompt": 0.00002, "completion": 0.0},
    "gpt-4o": {"prompt": 0.01, "completion": 0.03},
}

LOG_DIR = pathlib.Path("logs"); LOG_DIR.mkdir(exist_ok=True)


def instrument(model_name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator that times the wrapped fn and logs token cost."""
    price = PRICE[model_name]

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            t0 = time.perf_counter()
            resp = func(*args, **kwargs)
            elapsed_ms = round((time.perf_counter() - t0) * 1000)

            usage = getattr(resp, "usage", None)  # OpenAI objects expose usage
            prompt_t = usage.prompt_tokens if usage else 0
            comp_t   = usage.completion_tokens if usage else 0
            cost = round((prompt_t * price["prompt"] + comp_t * price["completion"]) / 1000, 6)

            log_obj = {
                "ts": dt.datetime.utcnow().isoformat() + "Z",
                "model": model_name,
                "elapsed_ms": elapsed_ms,
                "prompt_tokens": prompt_t,
                "completion_tokens": comp_t,
                "cost_usd": cost,
            }
            print("[metrics]", json.dumps(log_obj))
            LOG_DIR.joinpath(f"openai-{dt.date.today()}.jsonl").write_text(
                json.dumps(log_obj) + "\n", append=True
            )
            # attach metrics dict so caller can forward to headers
            resp._metrics = log_obj  # type: ignore[attr-defined]
            return resp
        return wrapper
    return decorator
```

---

## 2 · Wrap GPT‑4o call inside `/ask`

In `app/main.py` (Day 10 route) import and use the decorator:

```python
from app.metrics import instrument

# … inside /ask
@instrument("gpt-4o")
def _chat(user_prompt: str):
    return client.chat.completions.create(
        model=OA_MODEL,
        messages=[{"role": "user", "content": user_prompt}],
        temperature=0.7,
        max_tokens=160,
    )

try:
    resp = _chat(system_msg)
    answer = resp.choices[0].message.content.strip()
    usage  = resp.usage
    metrics = resp._metrics
except APIError:
    # … unchanged …

# replace previous cost / latency calc with metrics dict
res.headers.update({
    "X-Latency-MS": str(metrics["elapsed_ms"]),
    "X-Prompt-Tokens": str(metrics["prompt_tokens"]),
    "X-Completion-Tokens": str(metrics["completion_tokens"]),
    "X-Cost-USD": str(metrics["cost_usd"]),
})
```

Remove duplicate latency math you wrote yesterday (decorator handles it).

*(Optional) wrap the embedding call in `vector.py` using `@instrument("text-embedding-3-small")` for full coverage.*

---

## 3 · Re‑build & up backend

```bash
docker compose -f infra/compose.yaml build backend && docker compose up -d backend
```

---

## 4 · Smoke test & verify logs

```bash
curl -i -X POST http://localhost:8000/ask \
  -H 'Content-Type: application/json' \
  -d '{"page_id":1,"question":"What is the secret of the glyph?"}'
```

Expect headers `X-Latency-MS`, `X-Cost-USD` populated.
Check logs:

```bash
cat logs/openai-$(date +%F).jsonl | tail -1 | jq .
```

Should show JSON with tokens, cost, elapsed.

---

## 5 · CI unaffected (metrics only in runtime).

---

## 6 · Commit & PR

```bash
git checkout -b day12-metrics
git add apps/backend/app/metrics.py apps/backend/app/main.py logs/.gitignore
# add logs/.gitignore entry: logs/*
git commit -m "feat: metrics decorator logs OpenAI latency & cost"
git push -u origin day12-metrics
```

Open PR → **Closes #Day-12 issue** → merge after green.
Move project card to **Done**.

---

### ✅ End‑of‑Day 12 Definition

* Decorator logs JSON line per OpenAI call (embedding & chat).
* `/ask` exposes latency, token counts, and cost in headers.
* Log files written to `logs/openai-YYYY-MM-DD.jsonl` and ignored by Git.

*Tomorrow (Day 13):* enforce Ruff, Black, and ESLint via `pre-commit` and clean up style warnings.
