# Week 6 — Day 40 (Legal Pages & Footer Links)

> **Target session:** ≈ 1 h  **Goal:** publish placeholder legal documents—**Privacy Policy**, **Terms of Service**, and a **Delete‑Account** request form—then surface them via a footer on every page. Content can be plain‑text markdown with TODO notes for counsel review.
>
> **Outcome:** `/privacy`, `/tos`, and `/delete-account` routes load within the front‑end; footer on both desktop and mobile links to each. Delete‑account posts an email to `support@gibsey.com` for now.

---

## 1 · Create markdown pages

Add folder `apps/frontend/src/legal/` with:

### 1.1 `privacy.md`

```md
# Privacy Policy _(Draft)_

_Last updated: 13 May 2025_

Gibsey stores only the data required to power your reading & vault experience.

* Email address (for authentication)
* Questions you ask & answers generated (stored privately in your Vault)
* Usage metrics (anonymized) for improving latency & cost

**We do not sell your data.** Full policy will be reviewed by counsel before public launch.
```

### 1.2 `tos.md`

```md
# Terms of Service _(Draft)_

1. Gibsey is an alpha product; expect issues.
2. Content is provided “as‑is” without warranty.
3. You retain rights to your prompts & Vault entries.
4. Gibsey may revoke access for abuse.
```

### 1.3 `delete.md`

```md
# Delete Account Request _(Manual Alpha Flow)_

Email **support@gibsey.com** from the address associated with your account using subject line **“Delete My Gibsey Account”**. We’ll purge your data within 48 hours.
```

---

## 2 · Simple markdown renderer route

Add React component `src/routes/LegalPage.tsx`:

```tsx
import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";

export default function LegalPage({ doc }: { doc: string }) {
  const [md,setMd]=useState("Loading…");
  useEffect(()=>{ import(`../legal/${doc}.md?raw`).then(m=>setMd(m.default)); },[doc]);
  return (<main className="prose mx-auto p-4 dark:prose-invert"><ReactMarkdown>{md}</ReactMarkdown></main>);
}
```

Install renderer:

```bash
pnpm add react-markdown
```

Add Vite import for raw text in `vite.config.ts` if needed.

---

## 3 · Add routes to router

In `App.tsx` or React Router setup:

```tsx
import LegalPage from "./routes/LegalPage";
...
<Route path="/privacy" element={<LegalPage doc="privacy" />} />
<Route path="/tos" element={<LegalPage doc="tos" />} />
<Route path="/delete-account" element={<LegalPage doc="delete" />} />
```

---

## 4 · Footer component

`src/components/Footer.tsx`:

```tsx
export default function Footer(){
  return (
    <footer className="text-xs text-gray-500 dark:text-gray-400 mt-16 py-4 border-t flex justify-center gap-4">
      <a href="/privacy" className="hover:underline">Privacy</a>
      <span>·</span>
      <a href="/tos" className="hover:underline">Terms</a>
      <span>·</span>
      <a href="/delete-account" className="hover:underline">Delete Account</a>
    </footer>
  );
}
```

Insert `<Footer/>` below main content in `App.tsx`; add `mb-24` padding on mobile to avoid nav overlap.

---

## 5 · Mobile nav safe‑area tweak

Ensure `main` container ends with `pb-32 sm:pb-0` so content doesn’t collide with bottom nav + footer.

---

## 6 · Manual test

1. `/privacy` renders markdown; dark mode styles invert.
2. Footer links work on desktop & mobile; open in‑app route (no full reload).
3. Axe reports no new violations (links have discernible text).

---

## 7 · Commit & PR

```bash
git checkout -b day40-legal-pages
git add apps/frontend/src/legal apps/frontend/src/routes apps/frontend/src/components apps/frontend/src/App.tsx package.json pnpm-lock.yaml
git commit -m "feat: draft privacy/TOS/delete pages + footer links"
git push -u origin day40-legal-pages
```

PR → **Closes #Day‑40 issue** → merge when CI passes; move card to **Done**.

---

### ✅ End‑of‑Day 40 Definition

* `/privacy`, `/tos`, and `/delete-account` render markdown drafts.
* Footer links visible across layouts; no new a11y violations.

*Tomorrow (Day 41):* craft alpha invite email, limiter token, and feedback form.