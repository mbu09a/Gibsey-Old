# Week 3 — Day 20 (Dark‑Mode Theme & Mobile Polish)

> **Target session:** ≈ 2 h  **Goal:** enable Tailwind dark‑mode, add a UI toggle, and ensure the layout stacks cleanly on small screens (≤ 640 px). No new features—pure styling.
>
> **Outcome:** User can switch between light/dark themes; timeline, buttons, and inputs remain usable on phones; Lighthouse mobile score ≥ 90.

---

## 1 · Tailwind config for dark‑mode

Edit **`tailwind.config.js`**:

```js
export default {
  darkMode: "class",   // <‑‑ switch controlled via class
  content: ["./index.html", "./src/**/*.{ts,tsx,js,jsx}"],
  theme: {
    extend: {
      colors: {
        surface: {
          light: "#ffffff",
          dark: "#18181b", // zinc‑900-ish
        },
      },
    },
  },
  plugins: [],
};
```

---

## 2 · Theme toggle component

`src/components/DarkToggle.tsx`:

```tsx
import { Moon, Sun } from "lucide-react";
import { useEffect, useState } from "react";

export default function DarkToggle() {
  const [dark, setDark] = useState(() => localStorage.theme === "dark");

  useEffect(() => {
    const root = document.documentElement;
    if (dark) {
      root.classList.add("dark");
      localStorage.theme = "dark";
    } else {
      root.classList.remove("dark");
      localStorage.theme = "light";
    }
  }, [dark]);

  return (
    <button
      onClick={() => setDark(!dark)}
      className="p-2 rounded-full border dark:border-zinc-700 transition"
      title="Toggle dark mode"
    >
      {dark ? <Sun size={16} /> : <Moon size={16} />}
    </button>
  );
}
```

Add the toggle to the top‑bar (e.g., inside `App.tsx` header):

```tsx
<header className="flex justify-end p-2">
  <DarkToggle />
</header>
```

---

## 3 · Global background utility classes

In `index.css` after `tailwind` directives:

```css
html { background: theme("colors.surface.light"); }
html.dark { background: theme("colors.surface.dark"); }
```

Wrap main content container with `className="max-w-md mx-auto p-4"` to center on desktop but allow full width on mobile.

---

## 4 · Responsive tweaks

### 4.1 Timeline container

`className="space-y-6 max-h-[75vh] overflow-y-auto sm:max-h-96"`

### 4.2 Ask form button

Add `w-full sm:w-auto` so it fills width on mobile.

### 4.3 Flex layout

Ensure grid breaks:

```tsx
<div className="flex flex-col sm:flex-row gap-2">
  {/* inputs/buttons here */}
</div>
```

---

## 5 · Viewport meta (index.html)

```html
<meta name="viewport" content="width=device-width, initial-scale=1" />
```

---

## 6 · Lighthouse quick check

Use Chrome DevTools → Lighthouse → Mobile → run analysis. Aim for **Performance ≥ 90, Accessibility ≥ 90**.
If CLS due to image/icon sizing, add `min-w-[16px]` to icon buttons.

---

## 7 · Smoke tests

1. Toggle dark/light → backgrounds, text, and chips flip colors.
2. On phone emulator (iPhone SE), Ask form stacks vertically; buttons fill width.
3. Timeline scroll still works; chips readable.

---

## 8 · Commit & PR

```bash
git checkout -b day20-dark-mode
git add tailwind.config.js apps/frontend/src index.html src/components
git commit -m "feat: dark‑mode toggle and mobile responsive polish"
git push -u origin day20-dark-mode
```

Open PR → **Closes #Day‑20 issue** → merge when green.
Move card to **Done**.

---

### ✅ End‑of‑Day 20 Definition

* Tailwind dark‑mode via `.dark` class & toggle button.
* Mobile layout passes Lighthouse ≥ 90.
* No visual regressions on desktop light theme.

*Tomorrow (Day 21):* write Week‑3 retro, seed Week‑4 board, optionally point embed cron to 710‑page TSV.
