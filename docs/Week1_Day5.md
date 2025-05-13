# Week 1 — Day 5 (Frontend Shell)

> **Target session:** 1–2 h  **Focus:** scaffold a React app with Vite, load one shard via `/read?id=1`, and render title + content. Styling can stay bare‑bones; the win is proving front→back connectivity and measuring latency.

---

## 0 · Choose port & API base

We’ll serve the frontend at **[http://localhost:5173](http://localhost:5173)** (Vite default) and talk to FastAPI on **[http://localhost:8000](http://localhost:8000)**.
Add to `.env.example`:

```env
VITE_API_BASE=http://localhost:8000
```

---

## 1 · Create Vite app inside monorepo

```bash
cd apps/frontend
pnpm create vite@latest . --template react-ts  # or `npm`/`yarn`
# When prompted, name it "frontend".

pnpm install   # or npm/yarn
```

Add Tailwind via CDN in `index.html` head (skip full install tonight):

```html
<link href="https://cdn.tailwindcss.com" rel="stylesheet">
```

Commit scaffold:

```bash
git add .
git commit -m "frontend: vite-react scaffold"
```

---

## 2 · Add simple API helper

`src/lib/api.ts`:

```ts
export async function readPage(id: number) {
  const base = import.meta.env.VITE_API_BASE;
  const r = await fetch(`${base}/read?id=${id}`);
  if (!r.ok) throw new Error("Failed to fetch shard");
  return r.json();
}
```

---

## 3 · Replace default UI with fetch demo

Edit `src/App.tsx`:

```tsx
import { useState } from "react";
import { readPage } from "./lib/api";

function App() {
  const [page, setPage] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);
  const load = async () => {
    setLoading(true);
    try {
      const data = await readPage(1);
      setPage(data);
    } catch (e) {
      alert((e as Error).message);
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6 text-gray-800">
      <button
        onClick={load}
        className="mb-4 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50"
        disabled={loading}
      >
        {loading ? "Loading…" : "Fetch Shard"}
      </button>
      {page && (
        <article className="prose lg:prose-xl max-w-none">
          <h2>{page.title}</h2>
          <p>{page.content}</p>
        </article>
      )}
    </div>
  );
}
export default App;
```

Commit:

```bash
git add src
git commit -m "feat: fetch /read?id=1 and render"
```

---

## 4 · Wire frontend container (optional)

Add to `infra/compose.yaml`:

```yaml
  frontend:
    build: ../apps/frontend
    command: ["pnpm", "run", "dev", "--host", "0.0.0.0"]
    volumes:
      - ../apps/frontend:/usr/src/app
    ports: ["5173:5173"]
    environment:
      - VITE_API_BASE=http://localhost:8000
```

Dockerfile:

```dockerfile
FROM node:20-alpine
WORKDIR /usr/src/app
COPY . .
RUN corepack enable && pnpm install --frozen-lockfile
CMD ["pnpm", "run", "dev", "--host", "0.0.0.0"]
```

*(Skip container if you prefer local `pnpm run dev` during Week 1.)*

---

## 5 · Manual run & latency check

```bash
# terminal 1
docker compose -f infra/compose.yaml up -d backend db  # ensure API up

# terminal 2 (local dev)
cd apps/frontend
pnpm run dev
```

Open **[http://localhost:5173](http://localhost:5173)** → click **Fetch Shard** → shard text appears.
Open browser dev‑tools, watch *Network* timing — should complete in ≤ 200 ms backend + \~50 ms render (well under 2 s target).

---

## 6 · Placeholder ESLint in CI

Add at bottom of `.github/workflows/ci.yml` **frontend-lint** job:

```yaml
      - name: eslint stub
        run: npx -y eslint --init || true  # will exit 0 because not yet configured
```

*(Real lint rules land in Week 2 polish.)*

Commit & push as **day5-frontend-shell** branch:

```bash
git add infra apps/frontend .github
git commit -m "feat: day5 frontend shell + compose service"
git push --set-upstream origin day5-frontend-shell
```

Open PR → link to *Day 5* issue → merge when green.
Move board card **“Day 5 – React shell”** ➜ *Done*.

---

### ✅ End‑of‑Day 5 Definition

* `Fetch Shard` button loads shard 1 from FastAPI and renders.
* Manual latency check < 2 s total.
* Optional compose service makes full stack `docker compose up`‑able.

*Tomorrow (Day 6):* wire `/ask` endpoint, hook React form, and measure round‑trip.
