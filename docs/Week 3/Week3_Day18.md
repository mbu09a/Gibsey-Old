# Week 3 — Day 18 (Edit / Delete Vault Entries)

> **Target session:** ≈ 3 h  **Goal:** let the reader edit or delete their saved Q\&A. Provide safe backend endpoints and confirmation modals in the UI (Radix Dialog via shadcn/ui).
>
> **Outcome:** Timeline cards show ✏️ Edit & 🗑 Delete icons; actions update or remove the row and Realtime pushes the change to all open clients.

---

## 1 · Backend — REST endpoints

\### 1.1 DTOs (append to `app/schemas.py`)

```python
class VaultUpdateRequest(BaseModel):
    question: str | None = None
    answer: str | None = None
```

\### 1.2 Routes (`app/main.py`)

```python
from fastapi import HTTPException

@app.put("/vault/{vid}", response_model=VaultEntry)
async def vault_update(vid: int, req: VaultUpdateRequest):
    data = {k: v for k, v in req.model_dump().items() if v is not None}
    if not data:
        raise HTTPException(400, "No fields to update")
    res = (
        Supabase.client()
        .table("vault")
        .update(data)
        .eq("id", vid)
        .select()
        .single()
        .execute()
    )
    return res.data

@app.delete("/vault/{vid}", status_code=204)
async def vault_delete(vid: int):
    Supabase.client().table("vault").delete().eq("id", vid).execute()
```

*(Still no RLS; assume anon user for Week 3.)*

Re‑build backend:

```bash
docker compose -f infra/compose.yaml build backend && docker compose up -d backend
```

---

## 2 · Frontend — install shadcn/ui & icons

If not installed earlier:

```bash
cd apps/frontend
pnpm add @radix-ui/react-dialog @radix-ui/react-slot clsx lucide-react
```

---

## 3 · UI tweaks in `VaultTimeline`

\### 3.1 Add icon buttons to each card
Within the map loop:

```tsx
import { Pencil, Trash2 } from "lucide-react";
import * as Dialog from "@radix-ui/react-dialog";

// inside card div header
<div className="flex justify-between">
  <p className="text-xs text-gray-500">{date}</p>
  <div className="space-x-2">
    <button onClick={() => setEdit(e)}><Pencil size={16} /></button>
    <button onClick={() => onDelete(e.id)}><Trash2 size={16} /></button>
  </div>
</div>
```

*(style with Tailwind classes as desired)*

\### 3.2 Delete handler

```tsx
const onDelete = async (id:number) => {
  if(!confirm("Delete this entry?")) return;
  await fetch(`${import.meta.env.VITE_API_BASE}/vault/${id}`, { method:"DELETE" });
  setData(prev => prev.filter(p => p.id!==id));
};
```

\### 3.3 Edit modal (Radix Dialog)
Create `EditModal.tsx` component:

```tsx
interface Props { entry: Entry|null; onClose: () => void; }
export default function EditModal({entry,onClose}:Props){
  const [q,setQ]=useState(entry?.question||"");
  const [a,setA]=useState(entry?.answer||"");
  const save=async()=>{
    await fetch(`${import.meta.env.VITE_API_BASE}/vault/${entry!.id}`,{
      method:"PUT",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({question:q,answer:a})
    });
    onClose();
  };
  return(
    <Dialog.Root open={!!entry} onOpenChange={onClose}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/40"/>
        <Dialog.Content className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white p-6 rounded-md w-96 space-y-4">
          <Dialog.Title className="font-semibold">Edit Entry</Dialog.Title>
          <textarea className="w-full border p-2" value={q} onChange={e=>setQ(e.target.value)}/>
          <textarea className="w-full border p-2" value={a} onChange={e=>setA(e.target.value)}/>
          <div className="flex justify-end space-x-2">
            <button onClick={onClose} className="px-3 py-1">Cancel</button>
            <button onClick={save} className="px-3 py-1 bg-emerald-600 text-white">Save</button>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

In `VaultTimeline` keep `const [edit,setEdit]=useState<Entry|null>(null);` and render `<EditModal entry={edit} onClose={()=>setEdit(null)} />` at bottom.

*(Supabase Realtime will push update; but you can also patch local state after save.)*

---

## 4 · Test flow

1. Save a new Q\&A → timeline shows entry.
2. Click ✏️ → edit modal opens → change text → Save → modal closes.
3. Card updates automatically (Realtime) within 1 s.
4. Click 🗑 → confirm delete → entry disappears in all open tabs.

Check backend logs for Faust & Supabase update messages.

---

## 5 · Commit & PR

```bash
git checkout -b day18-edit-delete
git add apps/backend apps/frontend/src apps/frontend/src/components
# also add shadcn deps to package.json lock
git commit -m "feat: edit & delete Vault entries with Radix Dialog + endpoints"
git push -u origin day18-edit-delete
```

Open PR → **Closes #Day‑18 issue** → merge when green.
Move card to **Done**.

---

### ✅ End-of-Day 18 Definition

* Backend PUT & DELETE endpoints live.
* Timeline supports edit & delete with confirmation dialogs.
* Realtime still pushes all changes; latency < 2 s.

*Tomorrow (Day 19):* symbol chips, filter dropdown, and lucide icons polish.
