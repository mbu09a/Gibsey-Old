# Week 1 — Day 6 (End‑to‑End Round‑Trip)

> **Target session:** 3 h block  **Focus:** wire an `/ask` endpoint, hook a React form to it, and time the full Read → Ask round‑trip. Tonight is about plumbing, **not** model quality.
>
> **Outcome:** You can type a question, receive a JSON answer, and see total latency < 2 s.

---

## 0 · Pre‑flight

* `docker compose up backend db` is already running *or* you’ve got FastAPI on 8000 locally.
* Front‑end dev server (`pnpm run dev`) ready on 5173.

---

## 1 · Backend — add `/ask`

### 1.1  Pydantic DTOs

`apps/backend/app/schemas.py`:

```python
from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    page_id: int = Field(1, gt=0)          # default to shard 1 for now
    question: str = Field(..., min_length=1, max_length=512)

class AskResponse(BaseModel):
    answer: str
```

### 1.2  Route stub

In `app/main.py`:

```python
from .schemas import AskRequest, AskResponse
import time

@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    start = time.perf_counter()
    # 🚧  Placeholder answer — replace with real RAG later
    answer = (
        "[stub] I see you asked: ‘" + req.question.strip() + "’. "
        "Gibsey will reply in full once the Dream engine is online."
    )
    elapsed = (time.perf_counter() - start) * 1000
    print(f"/ask latency {elapsed:.0f} ms")
    return {"answer": answer}
```

*(Stretch‑goal snippet to call OpenAI chat is provided at bottom; keep off the critical path).*

### 1.3  Dependency bump & rebuild

No new deps needed; just rebuild container:

```bash
docker compose -f infra/compose.yaml build backend && docker compose up -d backend
```

---

## 2 · Front‑end — Ask form & latency timer

### 2.1  API helper

`src/lib/api.ts` — append:

```ts
export async function ask(question: string) {
  const base = import.meta.env.VITE_API_BASE;
  const t0 = performance.now();
  const r = await fetch(`${base}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, page_id: 1 }),
  });
  const json = await r.json();
  const t1 = performance.now();
  console.log(`🕒 /ask round‑trip: ${Math.round(t1 - t0)} ms`);
  return json;
}
```

### 2.2  UI update

In `src/App.tsx` replace the current component with:

```tsx
import { useState } from "react";
import { readPage, ask } from "./lib/api";

export default function App() {
  const [page, setPage] = useState<any | null>(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState<string | null>(null);
  const [loadingQ, setLoadingQ] = useState(false);

  const load = async () => {
    setPage(await readPage(1));
  };
  const submit = async () => {
    setLoadingQ(true);
    const resp = await ask(question);
    setAnswer(resp.answer);
    setLoadingQ(false);
  };

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <button onClick={load} className="px-4 py-2 bg-indigo-600 text-white rounded">
        Load Shard 1
      </button>

      {page && (
        <article className="prose">
          <h2>{page.title}</h2>
          <p>{page.content}</p>
        </article>
      )}

      {page && (
        <div className="space-y-4">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask Gibsey…"
            className="w-full border px-3 py-2 rounded"
          />
          <button
            onClick={submit}
            disabled={loadingQ || !question}
            className="px-4 py-2 bg-emerald-600 text-white rounded disabled:opacity-50"
          >
            {loadingQ ? "Thinking…" : "Ask"}
          </button>
          {answer && (
            <div className="border-l-4 border-emerald-600 pl-4 text-gray-800">
              <p>{answer}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
```

Commit:

```bash
git add src/lib/api.ts src/App.tsx
git commit -m "feat: /ask form with latency log"
```

---

## 3 · Manual test & latency target

1. **Terminal 1** — `docker compose up -d backend db` (if not already).
2. **Terminal 2** — `pnpm run dev` in `apps/frontend`.
3. Navigate to **localhost:5173** → Load shard → type question → click **Ask**.
4. Check browser console: */ask round‑trip* log should be **< 100 ms** (stub) — well under 2 s envelope.

If it spikes, ensure frontend `VITE_API_BASE` points to `http://localhost:8000`, not Docker hostname.

---

## 4 · CI note

No new workflow steps required; lint passes.

Push branch & PR:

```bash
git push -u origin day6-ask-loop
```

Link PR to **“Day 6 – E2E latency test”** → merge when green.
Move board card ➜ *Done*.

---

### ✅ End‑of‑Day 6 Definition

* POST `/ask` returns JSON `{answer}` within stub route.
* React form sends question and renders answer.
* Console log shows round‑trip < 2 s.

*Tomorrow (Day 7):* create `vault` table & endpoint, stub save, and hold a 30‑min retro.

---

## Stretch — plug in OpenAI for real answer (optional)

```python
from openai import OpenAI
client = OpenAI()

@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    page = (
        Supabase.client()
        .table("pages")
        .select("content")
        .eq("id", req.page_id)
        .single()
        .execute()
        .data
    )
    prompt = (
        "You are the narrator of a metafictional novel. "
        "Answer the reader’s question in ≤120 words, staying in‑world.\n\n"
        f"Shard:\n{page['content']}\n\nQuestion: {req.question}"
    )
    resp = client.chat.completions.create(model="gpt-4o", messages=[
        {"role": "user", "content": prompt}
    ])
    return {"answer": resp.choices[0].message.content.strip()}
```

Expect +500‑600 ms latency; still inside budget.
