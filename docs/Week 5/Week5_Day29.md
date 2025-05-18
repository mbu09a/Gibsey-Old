# Week 5 — Day 29 (Auth Modal & Supabase Session)

> **Target session:** ≈ 3 h  **Goal:** let users sign up / sign in with Supabase email *magic‑link*, store the session in localStorage, and show a small profile button when logged‑in.
>
> **Outcome:** Clicking **Sign in** opens a modal → user enters email → receives link → after confirmation, UI shows “You (name\@domain) · Logout”. No password fields yet.

---

\## 1 · Enable email auth in Supabase
1. Project → **Authentication ▸ Settings ▸ Email**.
2. Toggle **Email Link (magic link)** ON. Leave OTP & password OFF.
3. Set site URL to `http://localhost:5173`.
4. Save.

*(Supabase sends the link to its preview email UI in dev; production will send real email.)*

---

\## 2 · Install Supabase auth helpers in frontend

```bash
cd apps/frontend
pnpm add @supabase/auth-helpers-react @supabase/auth-helpers-shared
```

---

\## 3 · Create `AuthProvider` wrapper
`src/lib/Auth.tsx`:

```tsx
import { Session, createClientComponentClient } from "@supabase/auth-helpers-react";
import { createContext, useContext, useEffect, useState } from "react";
import { Database } from "../types/supabase";   // ← generate via Supabase types script later

const supabase = createClientComponentClient<Database>({
  supabaseUrl: import.meta.env.VITE_SUPABASE_URL!,
  supabaseKey: import.meta.env.VITE_SUPABASE_ANON_KEY!,
});

const AuthCtx = createContext<{ session: Session|null }|null>(null);
export const useAuth = () => useContext(AuthCtx)!;

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [session, setSession] = useState<Session|null>(supabase.auth.getSession().data.session);
  useEffect(() => {
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_e, s) => setSession(s));
    return () => subscription.unsubscribe();
  }, []);
  return <AuthCtx.Provider value={{ session }}>{children}</AuthCtx.Provider>;
}
export { supabase };
```

Wrap root in `main.tsx`:

```tsx
import { AuthProvider } from "./lib/Auth";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <AuthProvider>
      <App />
    </AuthProvider>
  </StrictMode>
);
```

---

\## 4 · Sign‑in modal (Radix Dialog)
`src/components/SignInModal.tsx`:

```tsx
import * as Dialog from "@radix-ui/react-dialog";
import { supabase } from "../lib/Auth";
import { useState } from "react";

export default function SignInModal() {
  const [open,setOpen] = useState(false);
  const [email,setEmail] = useState("");
  const [sent,setSent] = useState(false);
  const submit = async () => {
    const { error } = await supabase.auth.signInWithOtp({ email });
    if(!error) setSent(true);
  };
  return (
    <Dialog.Root open={open} onOpenChange={setOpen}>
      <Dialog.Trigger asChild>
        <button className="px-3 py-1 rounded-md border">Sign in</button>
      </Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/40" />
        <Dialog.Content className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white dark:bg-zinc-900 p-6 rounded-md w-80 space-y-4">
          <Dialog.Title className="font-semibold text-lg">Sign in / Sign up</Dialog.Title>
          {sent ? (
            <p>Check your email for a magic link.</p>
          ) : (
            <>
              <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="you@example.com" className="w-full border p-2 rounded-md" />
              <button onClick={submit} className="mt-3 w-full bg-emerald-600 text-white py-2 rounded-md">Send link</button>
            </>
          )}
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

---

\## 5 · Profile / logout button
Add to header (`App.tsx`):

```tsx
import { useAuth, supabase } from "./lib/Auth";
import SignInModal from "./components/SignInModal";
...
const { session } = useAuth();
<header className="flex justify-end gap-2 p-2">
  {session ? (
    <div className="flex items-center gap-2 text-sm">
      <span>{session.user.email}</span>
      <button onClick={()=>supabase.auth.signOut()} className="px-2 py-1 border rounded-md">Logout</button>
    </div>
  ) : (
    <SignInModal />
  )}
  <DarkToggle/>
</header>
```

---

\## 6 · Local test
1. Run dev server, click **Sign in**, enter your email (use your real or MailSlurp dev inbox).
2. Open the magic‑link email in Supabase Auth **→ Auth ▸ Users ▸ “Magic Link Preview”**.
3. Click the link → browser logs you in (url includes `#access_token=` fragment).
4. Header now shows `you@example.com · Logout`. Refresh → still logged‑in.

---

\## 7 · Commit & PR

```bash
git checkout -b day29-auth-modal
git add apps/frontend/src lib components tailwind.config.js package.json lockfile apps/frontend/vite.config.ts
# plus any .env.example additions
git commit -m "feat: Supabase magic‑link auth modal & session context"
git push -u origin day29-auth-modal
```

Open PR → **Closes #Day‑29 issue** → merge when green; move card to **Done**.

---

### ✅ End‑of‑Day 29 Definition

* Magic‑link modal sends email & stores session.
* Logged‑in email + logout shown in header.
* Session survives page refresh (localStorage managed by Supabase client).

*Tomorrow (Day 30):* add JWT guard to backend endpoints and write RLS policies for the Vault.