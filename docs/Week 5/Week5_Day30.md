# Week 5 — Day 30 (JWT Guard & Vault Row‑Level Security)

> **Target session:** ≈ 3 h  **Goal:** protect all write/read Vault endpoints with Supabase JWT verification on the backend **and** enforce Row‑Level Security so users can only access their own rows.
>
> **Outcome:** Hitting `/vault/*` without a valid `Authorization: Bearer <JWT>` header returns **401**; logged‑in users see only their own entries. Timeline shows zero items after logout.

---

## 1 · Back‑end — verify Supabase JWT

### 1.1 Install PyJWT helper

Append to `apps/backend/requirements.txt`:

```
python-jose[cryptography]>=3.3
```

Re‑build backend later.

### 1.2 Create `auth.py` dependency

`apps/backend/app/auth.py`:

```python
import os, requests
from fastapi import Depends, HTTPException, status, Header
from jose import jwt

SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
ISS = f"{os.getenv('SUPABASE_URL')}/auth/v1"

class User:  # minimal
    def __init__(self, sub: str, email: str):
        self.id = sub; self.email = email

def get_current_user(authorization: str = Header(...)) -> User:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")
    token = authorization.split()[1]
    try:
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"], issuer=ISS)
        return User(payload["sub"], payload.get("email", ""))
    except jwt.JWTError as e:
        raise HTTPException(401, "Invalid token") from e
```

Add env var `SUPABASE_JWT_SECRET` (found in Supabase Settings → API).

### 1.3 Guard routes

In `main.py`:

```python
from app.auth import get_current_user, User

@app.post("/vault/save", status_code=202)
async def save_to_vault(req: VaultSaveRequest, user: User = Depends(get_current_user)):
    payload = req.model_dump() | {"ts": time.time(), "user_id": user.id}
    await publish_gift(payload)
    return {"queued": True}

@app.get("/vault/list", response_model=list[VaultEntry])
async def vault_list(limit: int = 20, user: User = Depends(get_current_user)):
    data = (
        Supabase.client()
        .table("vault")
        .select("id,question,answer,created_at,symbol_id")
        .eq("user_id", user.id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute().data
    )
    return data
```

Repeat for update & delete.

---

## 2 · Database — add `user_id` & RLS

### 2.1 Column

```sql
alter table vault add column if not exists user_id uuid;
```

### 2.2 Enable RLS

```sql
alter table vault enable row level security;
create policy "Users can view own rows" on vault
  for select using (auth.uid() = user_id);
create policy "Users can insert" on vault
  for insert with check (auth.uid() = user_id);
create policy "Users can modify own rows" on vault
  for update using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "Users can delete own rows" on vault
  for delete using (auth.uid() = user_id);
```

Set table owner to service role if needed.

### 2.3 Change Faust worker insert

In `faust_worker.py` add `user_id` field from message payload; ensure message includes it (added in `/vault/save`).

---

## 3 · Front‑end — attach JWT to fetch

Update `api.ts` helper:

```ts
import { supabase } from "./lib/Auth";
export async function apiFetch(path:string, opts:RequestInit={}){
  const { data: { session } } = await supabase.auth.getSession();
  const headers = { ...(opts.headers||{}), 'Content-Type':'application/json' } as any;
  if(session) headers['Authorization'] = `Bearer ${session.access_token}`;
  const r = await fetch(`${import.meta.env.VITE_API_BASE}${path}`, { ...opts, headers });
  if(r.status===401) location.reload(); // crude logout
  return r;
}
```

Replace raw `fetch` calls with `apiFetch()`.

Timeline auto‑filters thanks to RLS no changes.

---

## 4 · Local test

1. **Logged‑out:** Timeline requests return 401 → empty screen.
2. **Logged‑in User A:** saves two entries.
3. Logout, login as User B (use second email) → cannot see User A entries.
4. User B cannot delete User A IDs (returns 404 due to RLS).

---

## 5 · Commit & PR

```bash
git checkout -b day30-jwt-rls
git add apps/backend/app/auth.py apps/backend/app/main.py apps/frontend/src/api.ts ...
# + migrations doc
git commit -m "feat: JWT guard on /vault/* and RLS policies (owner-only)"
git push -u origin day30-jwt-rls
```

PR → **Closes #Day-30 issue** → merge when CI passes; move card to **Done**.

---

### ✅ End-of-Day 30 Definition

* All Vault routes require valid Supabase JWT.
* Vault table RLS restricts rows to `user_id` owner.
* Front‑end automatically attaches token; logout clears timeline.

*Tomorrow (Day 31):* polish magic-link flow (resend, error toasts, expiry handling).