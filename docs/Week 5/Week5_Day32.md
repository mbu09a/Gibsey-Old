# Week 5 — Day 32 (Mobile Nav & Symbol Picker Polish)

> **Target session:** ≈ 2 h  **Goal:** deliver a smooth mobile UX: fixed bottom navigation bar on ≤ 640 px screens, a horizontally scrollable symbol‑filter bar, and small layout touches (safe‑area insets, tap targets ≥ 44 px).
>
> **Outcome:** On phones the app feels like a native reader: bottom nav gives quick access to **Read**, **Vault**, and **Settings**; symbol chips scroll horizontally and can be tapped with one thumb.

---

## 1 · Bottom navigation component

`src/components/MobileNav.tsx`:

```tsx
import { BookOpen, Clock, Settings } from "lucide-react";
import { useState } from "react";

const items = [
  { id: "read", icon: BookOpen, label: "Read" },
  { id: "vault", icon: Clock, label: "Vault" },
  { id: "settings", icon: Settings, label: "Settings" },
];
export default function MobileNav({ current, onChange }: { current: string; onChange: (id:string)=>void }) {
  return (
    <nav className="fixed bottom-0 inset-x-0 sm:hidden bg-white dark:bg-zinc-900 border-t flex justify-around pb-safe py-2">
      {items.map(it => (
        <button key={it.id} onClick={()=>onChange(it.id)} className={`flex flex-col items-center gap-1 text-xs ${current===it.id?"text-emerald-600":"text-gray-500"}`}>
          <it.icon size={20} />
          {it.label}
        </button>
      ))}
    </nav>
  );
}
```

*Note `pb-safe` uses Tailwind 3.4’s safe‑area inset plugin (ensure plugin enabled if needed).*

### 1.1 Wire into `App.tsx`

```tsx
const [view,setView]=useState("read");
...
<main className="pb-16 sm:pb-0">   {/* bottom‑nav space */}
  {view==="read" && <ReaderPane/>}
  {view==="vault" && <VaultTimeline/>}
  {view==="settings" && <SettingsPane/>}
</main>
<MobileNav current={view} onChange={setView}/>
```

Desktop (≥ sm) ignores nav because hidden via `sm:hidden`.

---

## 2 · Horizontal symbol picker

### 2.1 Component

`src/components/SymbolBar.tsx`:

```tsx
import { SYMBOLS } from "../lib/symbols";
import SymbolChip from "./SymbolChip";
export default function SymbolBar({ active, onPick }:{ active:number|"all"; onPick:(id:number|"all")=>void}){
  return (
    <div className="flex gap-2 overflow-x-auto px-2 py-1 no-scrollbar">
      <button onClick={()=>onPick("all")} className={`shrink-0 ${active==="all"?"ring-2 ring-emerald-500":""}`}>All</button>
      {SYMBOLS.map(s=> (
        <button key={s.id} onClick={()=>onPick(s.id)} className="shrink-0"><SymbolChip id={s.id}/></button>
      ))}
    </div>
  );
}
```

*Hide default scrollbar:* add `no-scrollbar` utility to `index.css`:

```css
.no-scrollbar::-webkit-scrollbar{display:none} .no-scrollbar{ -ms-overflow-style:none; scrollbar-width:none }
```

### 2.2 Replace dropdown in `VaultTimeline`

```tsx
const [filter,setFilter]=useState<number|"all">("all");
<SymbolBar active={filter} onPick={setFilter}/>
```

Dropdown from Day 19 can be kept for desktop (`hidden sm:block`) while symbol bar uses `sm:hidden` or vice‑versa.

---

## 3 · Tap‑target sizing & safe‑area

Add to global styles:

```css
button{ min-height:44px; min-width:44px; }
```

Check iPhone SE safe‑area bottom (simulator) – pb‑safe class reserves space.

---

## 4 · Accessibility check

Run `pnpm exec eslint` + Axe browser extension: verify nav buttons have `aria-label` if icon‑only; add `aria-current="page"` to active item.

---

## 5 · Manual mobile test

1. DevTools → iPhone 12 viewport.
2. Bottom nav shows, fixes to bottom, no viewport jump on keyboard.
3. Swipe symbol bar left/right, tap symbol → timeline filters quickly.
4. Rotate to landscape → nav still visible, content scroll area adjusts.

---

## 6 · Commit & PR

```bash
git checkout -b day32-mobile-nav
git add apps/frontend/src/components apps/frontend/src/index.css apps/frontend/src/App.tsx
git commit -m "feat: bottom mobile nav & horizontal symbol picker"
git push -u origin day32-mobile-nav
```

PR → **Closes #Day-32 issue** → merge when CI passes; move card to **Done**.

---

### ✅ End-of-Day 32 Definition

* Bottom nav appears only on small screens.
* Symbol chips scroll horizontally; dropdown remains for desktop.
* Tap‑targets meet 44 px, lighthouse A11y still ≥ 95.

*Tomorrow (Day 33):* accessibility audit with axe-core and fix remaining contrast / label issues.