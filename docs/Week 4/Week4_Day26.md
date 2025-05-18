# Week 4 — Day 26 (Loading Skeleton & Paging UI)

> **Target session:** ≈ 2 h  **Goal:** improve perceived performance by showing a shimmer loading skeleton while `/ask` is in flight, and add a *Load more* button to fetch additional results when the backend returns > 20 matches.
>
> **Outcome:** Users never stare at a blank screen; initial 20 hits render, and they can page through the rest without new API endpoints.

---

## 1 · Backend tweak — allow larger `k`

In `app/vector.py` temporarily bump default:

```python
async def similar_pages(text: str, k: int = 50):
```

*(50 vectors fits in Pinecone free tier and is enough for paging.)*
No route change—`/ask` already passes `k` from request (default 50 if omitted).

---

## 2 · Frontend — request bigger result set

In the Ask form handler (e.g., `submitAsk()`):

```ts
await fetch("/ask", { method:"POST", body: JSON.stringify({ question, k: 50, page_id }) })
```

Store `result.hits` (array) in a new `results` state.

---

## 3 · Loading skeleton component

`src/components/AskSkeleton.tsx`:

```tsx
export default function AskSkeleton() {
  return (
    <div className="space-y-4 animate-pulse" data-testid="skeleton">
      {[...Array(3)].map((_,i)=>(
        <div key={i} className="h-24 rounded-md bg-gray-300 dark:bg-zinc-700"/>
      ))}
    </div>
  );
}
```

Show while submitting:

```tsx
const [loading,setLoading]=useState(false);
...
setLoading(true);
const res = await submitAsk();
setLoading(false);
```

Render:

```tsx
{loading ? <AskSkeleton/> : <ResultsList hits={hitsSlice}/>}
```

---

## 4 · Paging state & Load more button

In `SearchResults` component:

```tsx
const [limit,setLimit] = useState(20);
const hitsSlice = hits.slice(0,limit);
...
{limit < hits.length && (
  <button onClick={()=>setLimit(l=>l+20)} className="mt-4 px-4 py-1 bg-zinc-200 dark:bg-zinc-700 rounded-md">
    Load more ({hits.length - limit} left)
  </button>
)}
```

*(If you prefer infinite scroll, wrap in intersection observer, but button is faster.)*

---

## 5 · Accessibility & visual polish

Add ARIA busy to skeleton container:

```tsx
<div aria-busy={loading}>{loading ? <AskSkeleton/> : ...}</div>
```

Ensure skeleton inherits dark-mode background.

---

## 6 · Manual test

1. Ask a broad question that returns > 20 hits (e.g., “What themes recur?”).
   *Expect:* three grey shimmer cards, then first 20 answers render.
2. Click **Load more** twice → all 50 hits display.
3. Lighthouse again—no CLS jump; performance unchanged.

---

## 7 · Commit & PR

```bash
git checkout -b day26-skeleton-paging
git add apps/frontend/src/components apps/frontend/src/*
# Update vector.py default k if committed
git add apps/backend/app/vector.py
git commit -m "feat: loading skeleton + Load more paging for results"
git push -u origin day26-skeleton-paging
```

Open PR → **Closes #Day‑26 issue** → merge when CI passes. Move card to **Done**.

---

### ✅ End‑of‑Day 26 Definition

* Shimmer skeleton visible during `/ask` fetch.
* First 20 hits render, *Load more* pages through remaining hits.
* No blank flashes; CLS < 0.1 in Lighthouse.

*Tomorrow (Day 27):* create cron monitor workflow to alert on embed failures & cost overruns.