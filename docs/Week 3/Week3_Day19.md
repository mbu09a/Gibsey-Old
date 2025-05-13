# Week 3 — Day 19 (Symbol Chips & Filter UI)

> **Target session:** ≈ 3 h  **Goal:** visually embed the *Corpus symbol* for each shard/Vault entry and let the reader filter timeline rows by symbol. Introduce lucide‑react icons and a dropdown filter component.
>
> **Outcome:** Each timeline card shows a colored chip (icon + label) derived from `symbol_id`; a dropdown at the top lets the user show *All* or a specific symbol—updates instantly via state.

---

## 1 · Define symbol map (frontend shared const)

Create `src/lib/symbols.ts` :

```ts
export type SymbolInfo = { id: number; name: string; color: string; icon: string };
export const SYMBOLS: SymbolInfo[] = [
  { id: 1,  name: "Seed",   color: "bg-emerald-600", icon: "Sprout" },
  { id: 2,  name: "Furnace", color: "bg-amber-600",  icon: "Flame" },
  // … add remaining 14 as you define them …
];
export const getSymbol = (id: number) => SYMBOLS.find(s => s.id === id) ?? SYMBOLS[0];
```

*(Icon names reference lucide‑react exports.)*

---

## 2 · Add lucide‑react to frontend

```bash
cd apps/frontend
pnpm add lucide-react
```

---

## 3 · Symbol Chip component

`src/components/SymbolChip.tsx`:

```tsx
import { getSymbol } from "../lib/symbols";
import * as icons from "lucide-react";

export default function SymbolChip({ id }: { id: number }) {
  const s = getSymbol(id);
  const Icon = (icons as any)[s.icon] ?? icons.Circle;
  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs text-white ${s.color}`}>
      <Icon size={12} />
      {s.name}
    </span>
  );
}
```

---

## 4 · Filter dropdown component

`src/components/SymbolFilter.tsx`:

```tsx
import { useState } from "react";
import { SYMBOLS } from "../lib/symbols";

export function useSymbolFilter() {
  const [filter, setFilter] = useState<number | "all">("all");
  return { filter, setFilter };
}

export default function SymbolFilter({ value, onChange }: { value: number | "all"; onChange: (v:number|"all")=>void }) {
  return (
    <select value={value} onChange={e=>onChange(e.target.value==="all"?"all":Number(e.target.value))} className="border p-1 rounded-md dark:bg-zinc-800">
      <option value="all">All Symbols</option>
      {SYMBOLS.map(s=> (
        <option key={s.id} value={s.id}>{s.name}</option>
      ))}
    </select>
  );
}
```

---

## 5 · Wire into `VaultTimeline`

Add:

```tsx
import SymbolChip from "./SymbolChip";
import SymbolFilter, { useSymbolFilter } from "./SymbolFilter";
```

Inside component:

```tsx
const { filter, setFilter } = useSymbolFilter();
```

Render dropdown above list:

```tsx
<div className="flex justify-end mb-2">
  <SymbolFilter value={filter} onChange={setFilter} />
</div>
```

Filter the displayed data:

```tsx
const visible = data.filter(d => filter === "all" || d.symbol_id === filter);
```

In the card markup, insert chip:

```tsx
<div className="flex items-center justify-between">
  <SymbolChip id={e.symbol_id} />
  <p className="text-xs text-gray-500">{date}</p>
</div>
```

Adjust styles as needed; chip color class comes from `SYMBOLS` map.

---

## 6 · Backend update (include symbol\_id in `/vault/save` payload)

Ensure `/vault/save` passes `symbol_id` when publishing to Kafka, and that the `vault` table already has a `symbol_id` column (add default 1 if missing):

```sql
alter table vault add column if not exists symbol_id int default 1;
```

Update publish payload in Day 16 code:

```python
payload = req.model_dump() | {"ts": time.time(), "symbol_id": req.symbol_id or 1}
```

*(Adjust `VaultSaveRequest` DTO to include `symbol_id`.)*

The consumer already inserts whatever fields exist.

---

## 7 · Manual test

1. Ask a question → choose **Save** → default symbol chip shows.
2. Call `/vault/save` manually with `"symbol_id":2` → chip color/label differs.
3. Use dropdown filter → list narrows correctly.

Latency still < 2 s end‑to‑end.

---

## 8 · Commit & PR

```bash
git checkout -b day19-symbol-ui
# add new components, constants, SQL migration note
git add apps/frontend/src components lib apps/backend
git commit -m "feat: symbol chips & filter dropdown in Vault timeline"
git push -u origin day19-symbol-ui
```

Open PR → **Closes #Day‑19 issue** → merge when green; move card to **Done**.

---

### ✅ End‑of‑Day 19 Definition

* Vault cards display symbol chips (icon + color).
* Dropdown filters timeline by symbol.
* Backend supports `symbol_id` in save payload.

*Tomorrow (Day 20):* Tailwind dark‑mode toggle + final mobile polish.
