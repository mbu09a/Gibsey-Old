# Week 7 — Day 45 (Vault Delete + Undo Flow)

> **Target session:** ≈ 3 h  **Goal:** let users delete a Vault entry with an immediate **Undo** snackbar. Implement a soft‑delete (`is_deleted` boolean) so data sticks around for 24 h, then hard‑purge via nightly cron.
>
> **Outcome:** Trash icon removes an entry, toast appears *“Entry deleted — Undo”*; clicking undo restores it. Cron job cleans up old soft‑deleted rows daily. Latency unchanged.

---

## 1 · Database — add soft‑delete flag

```sql
alter table vault add column if not exists is_deleted boolean default false;
create index if not exists vault_not_deleted on vault(id) where is_deleted = false;
```

Update RLS `select` policy to `AND is_deleted = false`.

---

## 2 · Backend routes

### 2.1 Delete endpoint

```python
class VaultDeleteRequest(BaseModel):
    id: int

@app.post("/vault/delete", status_code=204)
async def vault_delete(req: VaultDeleteRequest, user: User = Depends(get_current_user)):
    sb.table("vault").update({"is_deleted": True, "deleted_at": datetime.utcnow()}) \
        .eq("id", req.id).eq("user_id", user.id).execute()
```

### 2.2 Undo endpoint

```python
@app.post("/vault/undo", status_code=200)
async def vault_undo(req: VaultDeleteRequest, user: User = Depends(get_current_user)):
    sb.table("vault").update({"is_deleted": False, "updated_at": datetime.utcnow()}) \
        .eq("id", req.id).eq("user_id", user.id).execute()
    return {"ok": True}
```

---

## 3 · Nightly purge cron

Add script `scripts/purge_deleted.py`:

```python
from datetime import datetime, timedelta
from supabase import create_client
import os
sb=create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))
cutoff=datetime.utcnow()-timedelta(hours=24)
sb.table("vault").delete().lt("deleted_at", cutoff.isoformat()).execute()
```

Workflow `.github/workflows/purge.yml` scheduled `cron: '15 5 * * *'` runs script via docker‑compose service.

---

## 4 · Front‑end

### 4.1 Trash icon & optimistic removal

In `VaultEntry.tsx`:

```tsx
import { Trash2 } from "lucide-react";
...
<button aria-label="Delete" onClick={()=>deleteEntry(entry)} className="p-1"><Trash2 size={16}/></button>
```

`deleteEntry`:

```tsx
import toast from "react-hot-toast";
async function deleteEntry(e:Entry){
  setVault(v=>v.filter(x=>x.id!==e.id));  // optimistic
  await apiFetch("/vault/delete", {method:"POST", body:JSON.stringify({id:e.id})});
  toast.custom(t=> <UndoToast t={t} entry={e}/>, { duration:5000 });
}
```

### 4.2 UndoToast component

```tsx
function UndoToast({ t, entry }:{ t:any, entry:Entry }){
  return <div className="bg-gray-800 text-white px-4 py-2 rounded-md flex gap-2">
    <span>Entry deleted.</span>
    <button onClick={async()=>{
      await apiFetch("/vault/undo",{method:"POST",body:JSON.stringify({id:entry.id})});
      setVault(v=>[entry,...v]); toast.dismiss(t.id);
    }} className="underline">Undo</button>
  </div>;
}
```

---

## 5 · Supabase Realtime filter

Ensure subscription query includes `is_deleted = false` condition so deletes auto‑remove from other tabs.

---

## 6 · Tests

* Pytest: user A deletes → is\_deleted true; user B cannot undo.
* Bench: confirm `/vault/delete` < 200 ms.

---

## 7 · Manual QA

1. Delete entry → vanishes immediately.
2. Undo within 5 s returns entry.
3. Reload page → entry state persists accordingly.
4. Wait > 24 h or modify `deleted_at` to past → cron removes row.

---

## 8 · Commit & PR

```bash
git checkout -b day45-vault-delete
# add backend routes, script, workflow, front-end changes
git add apps/backend scripts/purge_deleted.py apps/frontend
git commit -m "feat: vault soft-delete with undo and nightly purge"
git push -u origin day45-vault-delete
```

PR → **Closes #Day-45 issue** → merge after CI; update changelog; move card to **Done**.

---

### ✅ End-of-Day 45 Definition

* Delete & Undo flow works; audit table unchanged.
* Nightly purge cron job committed and scheduled.
* Latency & RLS unaffected.

*Tomorrow (Day 46):* implement 16‑symbol palette with color trails.