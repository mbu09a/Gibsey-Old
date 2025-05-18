# Week 5 — Day 31 (Magic‑Link Flow Polish & Expiry Handling)

> **Target session:** ≈ 2 h  **Goal:** smooth out the authentication UX: add a **resend link** timer, toast notifications for success/error, and a top‑bar banner if the JWT expires while the user is browsing.
>
> **Outcome:** Users get immediate feedback when requesting a link, can’t spam resend for 60 s, and see a “Session expired – please sign in again” banner without silent 401 failures.

---

## 1 · Add toast provider

Install **react‑hot‑toast** (lightweight):

```bash
cd apps/frontend
pnpm add react-hot-toast
```

Wrap root in `main.tsx`:

```tsx
import { Toaster } from "react-hot-toast";
...
<AuthProvider>
  <App />
  <Toaster position="top-center" toastOptions={{ duration: 4000 }} />
</AuthProvider>
```

---

## 2 · Enhance `SignInModal`

### 2.1 State & timer

```tsx
const [cooldown,setCooldown] = useState(0);
useEffect(()=>{
  if(!cooldown) return; const id=setInterval(()=>setCooldown(c=>c-1),1000);
  return ()=>clearInterval(id);
},[cooldown]);
```

### 2.2 Submit with toast

```tsx
import toast from "react-hot-toast";
...
const submit = async () => {
  const { error } = await supabase.auth.signInWithOtp({ email, options:{ emailRedirectTo: window.location.origin } });
  if(error) return toast.error(error.message);
  toast.success("Magic link sent! Check your inbox.");
  setSent(true); setCooldown(60);
};
```

### 2.3 Resend link button

```tsx
{sent && (
  <button disabled={cooldown>0} onClick={submit} className="text-sm underline disabled:opacity-40">
    {cooldown ? `Resend in ${cooldown}s` : "Resend link"}
  </button>
)}
```

---

## 3 · Global session‑expiry banner

`src/components/SessionBanner.tsx`:

```tsx
import { useAuth } from "../lib/Auth";
import { useEffect, useState } from "react";
export default function SessionBanner(){
  const { session } = useAuth();
  const [expired,setExpired] = useState(false);
  useEffect(()=>{
    if(!session) return; // no login yet
    const expMs = session.expires_at*1000 - Date.now();
    const id = setTimeout(()=>setExpired(true), expMs);
    return ()=>clearTimeout(id);
  },[session]);
  if(!expired) return null;
  return (
    <div className="bg-amber-500 text-white text-center py-2 text-sm">
      Session expired — <button onClick={()=>location.reload()} className="underline font-medium">sign in again</button>
    </div>
  );
}
```

Add `<SessionBanner/>` just inside `<AuthProvider>` or at top of `App.tsx`.

---

## 4 · Update `apiFetch` 401 handling

Replace hard reload with toast + redirect to sign‑in:

```ts
if(r.status===401){
  toast.error("Please sign in again.");
  supabase.auth.signOut();
  return Promise.reject("unauthenticated");
}
```

Modal auto‑appears because header shows Sign in when session null.

---

## 5 · Manual test checklist

1. **Request link** → green toast → button disabled 60 s.
2. Open link from email preview → logged in, header shows email.
3. Wait until token expiry (default 1 hr) or edit JWT exp locally to 5 min → banner appears, 401 toast fired on next API call.
4. Click *sign in again* → modal opens.

---

## 6 · Commit & PR

```bash
git checkout -b day31-magiclink-polish
git add apps/frontend/src/lib apps/frontend/src/components apps/frontend/src/main.tsx package.json pnpm-lock.yaml
git commit -m "feat: magic-link resend cooldown, toast feedback, session-expiry banner"
git push -u origin day31-magiclink-polish
```

Open PR → **Closes #Day-31 issue** → merge when CI passes; move card to **Done**.

---

### ✅ End-of-Day 31 Definition

* Resend link cooldown + toasts.
* Session expiry banner prompts re-login.
* 401s handled gracefully without blank UI.

*Tomorrow (Day 32):* craft mobile nav bar and scrollable symbol picker polish.