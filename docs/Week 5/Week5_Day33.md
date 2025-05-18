# Week 5 — Day 33 (Accessibility Audit & Fixes)

> **Target session:** ≈ 2 h  **Goal:** run automated a11y checks (axe-core + Lighthouse), remedy any color‑contrast, label, or keyboard‑nav issues, and document an accessibility statement. Target score: **Lighthouse Accessibility ≥ 95** on both mobile and desktop.
>
> **Outcome:** Zero critical axe violations; lighthouse a11y ≥ 95; tab order logical; all interactive elements have names/roles; README contains a short accessibility note.

---

## 1 · Automated audit setup

\### 1.1 Install axe-core React hook

```bash
cd apps/frontend
pnpm add -D @axe-core/react
```

Wrap in dev only (`src/main.tsx`):

```tsx
if (import.meta.env.DEV) {
  import("@axe-core/react").then(({ default: axe }) =>
    axe(React, ReactDOM, 1000)
  );
}
```

This logs violations to console while running `pnpm run dev`.

\### 1.2 Add lighthouse CI script (optional)

```bash
pnpm add -D @lhci/cli
```

`package.json` script:

```json
"lhlocal": "lhci autorun --collect.url=http://localhost:5173 --collect.numberOfRuns=1"
```

---

\## 2 · Run audits & fix issues

1. `pnpm run dev` → open DevTools console; axe logs violations.

2. Common fixes:

   * **Color contrast:** tweak Tailwind colors: `text-gray-500` → `text-gray-600`; ensure chips pass contrast in dark mode (use `text-white/90`).
   * **Accessible names:** add `aria-label` to icon‑only buttons in `MobileNav`, `Edit/Delete` icons.
   * **Heading order:** ensure `h1` on top (App title) then `h2` sections.
   * **Keyboard focus:** add `focus:outline-none focus:ring` classes to buttons & chips.
   * **Role / landmark:** wrap main content in `<main>`; header in `<header>`; nav bar already `<nav>`.

3. After each fix, refresh → axe should log **0 critical, 0 serious**.

4. Lighthouse run (new terminal):

```bash
pnpm run lhlocal
```

Verify **Accessibility ≥ 95**. If not, click report, scroll to failing audits, patch accordingly.

---

\## 3 · Accessibility statement
Add `docs/ACCESSIBILITY.md`:

```md
# Accessibility Commitment

Gibsey aims to meet **WCAG 2.1 AA** standards. Key points:
* Color-contrast ratios ≥ 4.5:1 (large text ≥ 3:1).
* All navigation & controls operable via keyboard.
* ARIA labels provided for icon buttons, dialogs, and dynamic content.
* Screen‑reader live regions (`aria-busy`, toast updates) announce state changes.

We run automated audits (axe-core & Lighthouse) on each pull request. Please file issues for any barriers encountered.
```

Link from main README: `See our [accessibility commitment](docs/ACCESSIBILITY.md).`

---

\## 4 · CI integration
Add step to `ci.yml` after build:

```yaml
- name: axe run
  run: pnpm exec axe --exit
  # simple CLI using playwright + axe; or skip if no viewport available
```

*(Use `axe-core/playwright` if you want headless checks.)*
Optional: require lighthouse CI on PR (> 95) but may slow pipeline.

---

\## 5 · Keyboard‑nav sanity
Manual checklist: tab through entire page → focus visible; Enter activates buttons; Esc closes modals.

---

\## 6 · Commit & PR

```bash
git checkout -b day33-a11y-audit
git add apps/frontend docs/ACCESSIBILITY.md README.md .github/workflows/ci.yml
git commit -m "chore: axe/lighthouse a11y fixes & statement (score ≥ 95)"
git push -u origin day33-a11y-audit
```

PR → **Closes #Day-33 issue** → merge when CI passes; move card to **Done**.

---

### ✅ End‑of‑Day 33 Definition

* axe logs **0 serious+ violations** in dev.
* Lighthouse Accessibility ≥ 95 mobile & desktop.
* Accessibility statement committed.

*Tomorrow (Day 34):* wire Grafana dashboard for token cost and daily usage.