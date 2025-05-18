# Week 7 — Day 46 (16‑Symbol Palette & Trail Animation)

> **Target session:** ≈ 3 h  **Goal:** visually distinguish all 16 Corpus symbols with unique **color + rotation trail** chips. Replace the placeholder 2‑symbol set everywhere: symbol picker, card borders, and mini‑icon next to answers. Animation must stay GPU‑cheap (1 transform, 30 fps, prefers‑reduced‑motion safe).
>
> **Outcome:** The SymbolBar shows a colorful ring for each of the 16 symbols; choosing one highlights it with a slow‑rotating trail. Answer cards carry a left‑border stripe in the same hue. Lighthouse and Axe remain clean; trace reveals < 1 % long‑task time.

---

\## 1 · Design the palette
Add `src/lib/symbols.ts`:

```ts
export interface SymbolMeta { id: number; name: string; hue: number; }
export const SYMBOLS: SymbolMeta[] = [
  { id: 1,  name: "Fountain",       hue: 180 },
  { id: 2,  name: "Key",            hue: 30  },
  { id: 3,  name: "Mirror",         hue: 260 },
  { id: 4,  name: "Path",           hue: 110 },
  // ... continue through 16, picking visually distinct hues
];
export const hueToTailwind = (h: number) => `hsl(${h} 75% 60%)`; // runtime style
```

---

\## 2 · SVG trail chip component
`src/components/SymbolChip.tsx`:

```tsx
import { SYMBOLS, hueToTailwind } from "../lib/symbols";
import { motion } from "framer-motion";
export default function SymbolChip({ id, active }:{ id:number; active?:boolean }){
  const meta = SYMBOLS.find(s=>s.id===id)!;
  const size = active? 42: 36;
  const dash = active? 95: 120;
  return (
    <motion.svg width={size} height={size} viewBox="0 0 100 100" animate={{ rotate: active? 360: 0 }} transition={{ repeat:active? Infinity:0, duration:20, ease:"linear" }}
      className="shrink-0">
      <circle r="40" cx="50" cy="50" fill="transparent" stroke={hueToTailwind(meta.hue)} strokeWidth="8" strokeDasharray={`${dash} 250`} strokeLinecap="round" />
    </motion.svg>
  );
}
```

*Animation guard:* wrap animation in `@media (prefers-reduced-motion: no-preference)` via Tailwind plugin or early return.

---

\## 3 · Integrate into SymbolBar & picker
Replace previous chip mapping:

```tsx
{SYMBOLS.map(s=> (
  <button key={s.id} onClick={()=>onPick(s.id)} aria-label={s.name}
     className={`${active===s.id?"ring-2 ring-emerald-500":""}`}>
     <SymbolChip id={s.id} active={active===s.id} />
  </button>
))}
```

---

\## 4 · Card border & answer trail
In `AnswerCard.tsx` add runtime style border color:

```tsx
const color = hueToTailwind(SYMBOLS.find(s=>s.id===answer.symbol_id)!.hue);
<div style={{ borderLeft:`4px solid ${color}` }} ...>
```

If dark mode contrast low, lighten with `hsl(hue 80% 70%)`.

---

\## 5 · Accessible contrast & motion test

1. **Contrast:** Run Axe; adjust L values to meet 3:1 against white/dark.
2. **prefers‑reduced‑motion:** In devtools, toggle setting—chips stop rotating.
3. **GPU audit:** Chrome Performance record 10 s scroll; ensure minimal paint.

---

\## 6 · Latency sanity
Run bench script (`scripts/bench.py`)—should show no change (UI‑only work). Document in PR.

---

\## 7 · Commit & PR

```bash
git checkout -b day46-symbol-palette
# add symbols lib, chip component, bar/card updates
git add apps/frontend/src/lib/symbols.ts apps/frontend/src/components/SymbolChip.tsx apps/frontend/src/components/SymbolBar.tsx apps/frontend/src/components/AnswerCard.tsx
# plus Tailwind plugin for reduced‑motion if added
git commit -m "feat: 16‑symbol palette with color trails & low‑motion rotation"
git push -u origin day46-symbol-palette
```

PR → **Closes #Day-46 issue** → merge when CI & Axe pass; move card to **Done**.

---

\### ✅ End‑of‑Day 46 Definition

* Symbol picker shows 16 colorful chips; active chip slow‑rotates.
* Answer cards display matching color stripe.
* prefers‑reduced‑motion disables animation; Lighthouse A11y ≥ 95.

*Tomorrow (Day 47):* enable filter logic & latency benchmark (already planned).