# Week 2 — Day 11 (Vault Timeline & Tailwind Full Install)

> **Target session:** ≈ 2 h  **Goal:** list the reader’s saved Q\&A in the UI and move the frontend from CDN Tailwind to a local Tailwind + shadcn/ui setup.
>
> **Outcome:** `/vault/list` paginates results; React shows the latest 20 entries below the Ask form; Tailwind CLI & shadcn/ui are fully installed.

---

## 1 · Backend ­— `/vault/list` endpoint

### 1.1  Schema update

`app/schemas.py`:

```python
from pydantic import BaseModel, Field
from datetime import datetime

class VaultEntry(BaseModel):
    id: int
    question: str
    answer: str
    created_at: datetime
```

### 1.2  Route in `app/main.py`

```python
from typing import List

@app.get("/vault/list", response_model=List[VaultEntry])
async def vault_list(page: int = 1, limit: int = 20):
    offset = (page - 1) * limit
    data = (
        Supabase.client()
        .table("vault")
        .select("id,question,answer,created_at")
        .order("created_at", desc=True)
        .range(offset, offset + limit - 1)
        .execute()
        .data
    )
    return data
```

*(No auth yet — returns all rows.)*

### 1.3  Re‑build backend

```bash
docker compose -f infra/compose.yaml build backend && docker compose up -d backend
```

---

## 2 · Frontend — switch to local Tailwind + shadcn/ui

### 2.1  Install Tailwind & init config

```bash
cd apps/frontend
pnpm add -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

Edit `tailwind.config.js`:

```js
export default {
  content: [
    "./index.html",
    "./src/**/*.{ts,tsx,js,jsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

Replace CDN link in `index.html` with:

```html
<script type="module" src="/src/main.tsx"></script>
```

Create `src/index.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Import it in `main.tsx`:

```ts
import "./index.css";
```

### 2.2  Install shadcn/ui & lucide-react

```bash
pnpm add @radix-ui/react-slot clsx lucide-react
```

For now we’ll just use native Tailwind classes; shadcn components land Week 3.

---

## 3 · React ­— `VaultTimeline` component

`src/components/VaultTimeline.tsx`:

```tsx
import { useEffect, useState } from "react";
interface Entry { id: number; question: string; answer: string; created_at: string; }

export default function VaultTimeline() {
  const [data, setData] = useState<Entry[]>([]);
  const fetchEntries = async () => {
    const r = await fetch(`${import.meta.env.VITE_API_BASE}/vault/list?limit=20`);
    setData(await r.json());
  };
  useEffect(() => { fetchEntries(); }, []);
  return (
    <section className="mt-10 space-y-6 max-h-96 overflow-y-auto" id="vault">
      {data.map(e => (
        <div key={e.id} className="p-4 border rounded-md bg-white shadow-sm">
          <p className="text-sm text-gray-500">{new Date(e.created_at).toLocaleString()}</p>
          <p className="font-semibold">Q: {e.question}</p>
          <p className="mt-2 text-gray-800">A: {e.answer}</p>
        </div>
      ))}
    </section>
  );
}
```

### 3.1  Embed in `App.tsx`

```tsx
import VaultTimeline from "./components/VaultTimeline";
// … inside JSX after the Ask form
<VaultTimeline />
```

*(Auto‑scroll stretch: `useEffect(() => { ref.current?.scrollIntoView({behavior:"smooth"}); }, [data]);` if desired.)*

---

## 4 · Frontend dev test

```bash
pnpm run dev
# open http://localhost:5173, save a new Q&A, refresh Vault list should show entry
```

---

## 5 · Commit & PR

```bash
# backend + frontend changes
 git checkout -b day11-vault-timeline
 git add apps/frontend apps/backend/app/index.css tailwind.config.js
 git commit -m "feat: vault list endpoint + timeline UI, local Tailwind setup"
 git push -u origin day11-vault-timeline
```

Open PR → **Closes #Day‑11 issue** → merge after green CI.
Move project card to **Done**.

---

### ✅ End‑of‑Day 11 Definition

* `/vault/list` paginated endpoint working.
* React shows latest 20 Vault entries.
* Tailwind CLI & config replace CDN; build works locally.

*Tomorrow (Day 12):* add latency & cost logging wrapper for OpenAI calls and write to JSONL file.
