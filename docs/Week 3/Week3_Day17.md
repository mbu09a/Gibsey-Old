# Week 3 — Day 17 (Realtime Vault Timeline)

> **Target session:** ≈ 2 h  **Goal:** push new Vault entries to the UI instantly using **Supabase Realtime**; fall back to 5 s polling if WebSocket disconnects.
>
> **Outcome:** When a `/vault/save` request is queued → Kafka → Faust → DB, the timeline on any open page updates within \~250 ms, no manual refresh.

---

## 1 · Enable Realtime on the `vault` table (Supabase UI)

1. In *app.supabase.com* open your project → **Database** → **Tables** → `vault`.
2. Click the **Realtime** tab → toggle **“Realtime on”**.
3. Supabase auto‑creates the replication publication.

*(RLS is still OFF, so anon key can subscribe. No further SQL needed.)*

---

## 2 · Install Supabase JS client in the frontend

```bash
cd apps/frontend
pnpm add @supabase/supabase-js
```

Add env variable to **`.env.example`** (front‑end):

```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=<anon-key>
```

Update your local `.env` with real values.

---

## 3 · Create a singleton Supabase client

`src/lib/sbClient.ts`:

```ts
import { createClient } from "@supabase/supabase-js";

export const supabase = createClient(
  import.meta.env.VITE_SUPABASE_URL!,
  import.meta.env.VITE_SUPABASE_ANON_KEY!
);
```

---

## 4 · Upgrade `VaultTimeline` component

```tsx
import { useEffect, useState, useRef } from "react";
import { supabase } from "../lib/sbClient";
interface Entry { id:number; question:string; answer:string; created_at:string; }

export default function VaultTimeline() {
  const [data, setData] = useState<Entry[]>([]);
  const endRef = useRef<HTMLDivElement>(null);

  // initial fetch + realtime subscription
  useEffect(() => {
    const fetchInitial = async () => {
      const r = await fetch(`${import.meta.env.VITE_API_BASE}/vault/list?limit=20`);
      setData(await r.json());
    };
    fetchInitial();

    const sub = supabase
      .channel("vault_changes")
      .on(
        "postgres_changes",
        { event: "INSERT", schema: "public", table: "vault" },
        (payload) => setData((prev) => [payload.new as Entry, ...prev.slice(0,19)])
      )
      .subscribe();

    return () => { supabase.removeChannel(sub); };
  }, []);

  // auto‑scroll to newest
  useEffect(() => { endRef.current?.scrollIntoView({ behavior: "smooth" }); }, [data]);

  if (!data.length) return <p className="text-gray-500">No entries yet.</p>;
  return (
    <section className="mt-10 space-y-6 max-h-96 overflow-y-auto" id="vault">
      {data.map(e => (
        <div key={e.id} className="p-4 border rounded-md bg-white dark:bg-zinc-800 shadow-sm">
          <p className="text-xs text-gray-500 dark:text-zinc-400">{new Date(e.created_at).toLocaleString()}</p>
          <p className="font-semibold">Q: {e.question}</p>
          <p className="mt-2">A: {e.answer}</p>
        </div>
      ))}
      <div ref={endRef} />
    </section>
  );
}
```

*(The slice keeps the list to 20 entries.)*

---

## 5 · Fallback polling (30 s)

Add inside the same `useEffect` after subscription:

```tsx
const poll = setInterval(fetchInitial, 30000);
return () => { clearInterval(poll); supabase.removeChannel(sub); };
```

---

## 6 · Dev test

1. Run `docker compose up -d` for backend, kafka, faust.
2. `pnpm run dev` for frontend.
3. Open **two** browser tabs at `localhost:5173`.
4. In tab 1, Ask and **Save to Vault**.
5. Within < 1 s the timeline in **tab 2** should show the new entry.

Check console for any Supabase channel errors; if WebSocket disconnects, the polling fallback should still update within 30 s.

---

## 7 · Commit & PR

```bash
git checkout -b day17-realtime-vault
git add apps/frontend src/lib apps/frontend/src/components
git commit -m "feat: realtime Vault timeline via Supabase channel + polling fallback"
git push -u origin day17-realtime-vault
```

Open PR → **Closes #Day-17 issue** → merge once CI passes.
Move card to **Done**.

---

### ✅ End-of-Day 17 Definition

* Supabase Realtime channel active; new Vault entries push to all open clients.
* Fallback polling guarantees eventual consistency.
* Auto‑scroll keeps newest entry in view.

*Tomorrow (Day 18):* add delete & edit endpoints + UI modal dialogs.
