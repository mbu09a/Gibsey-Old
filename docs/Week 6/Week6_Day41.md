# Week 6 — Day 41 (Alpha Invite & Onboarding Guide)

> **Target session:** ≈ 2 h  **Goal:** craft the alpha‑tester onboarding flow: unique invite tokens (limited to 25 sign‑ups), a concise welcome email with Loom walkthrough video, and a feedback Google Form accessible from the app’s footer.
>
> **Outcome:** Sending the email invites lets exactly 25 users register; new users land on a welcome screen with quick tips; feedback form link is live. All data tracked in Airtable/Sheet for follow‑up.

---

## 1 · Generate invite tokens table

Create a small table in Supabase (or simple JSON list) to gate alpha:

```sql
create table if not exists invites (
  token text primary key,
  claimed_by uuid,
  claimed_at timestamptz
);
```

Generate 25 random 6‑char tokens:

```python
import secrets, string, csv, sys
alphabet=string.ascii_uppercase+string.digits
rows=[[ ''.join(secrets.choice(alphabet) for _ in range(6)) ] for _ in range(25)]
writer=csv.writer(sys.stdout); writer.writerows(rows)
```

Insert into `invites` along with NULL user.

---

## 2 · Modify sign‑in flow to require token once

Add an *Invite Code* prompt to `SignInModal` (only on first login):

```tsx
const [invite,setInvite]=useState("");
...
if(!invite) return toast.error("Invite code required");
```

After Supabase session established, verify token:

```tsx
const { data } = await apiFetch("/invite/claim", { method:"POST", body: JSON.stringify({ token: invite }) });
```

Backend route:

```python
@app.post("/invite/claim")
async def claim_invite(req: InviteRequest, user: User = Depends(get_current_user)):
    token=req.token.upper()
    row = sb.table("invites").select("claimed_by").eq("token",token).single().execute().data
    if not row or row["claimed_by"] not in (None, user.id):
        raise HTTPException(403, "Invalid or used token")
    sb.table("invites").update({"claimed_by": user.id, "claimed_at": datetime.utcnow()}).eq("token",token).execute()
    return {"ok": True}
```

After first success, store flag in localStorage so modal hides code field on subsequent logins.

---

## 3 · Welcome screen / tooltip tour

After first successful login (check `localStorage.getItem("first_launch") === null`):

```tsx
toast.success("Welcome to the Gibsey alpha! Read the preface, ask anything, then save to your Vault.");
localStorage.setItem("first_launch","done");
```

Optional: use Shepherd.js for step‑by‑step tooltips (skip if short on time).

---

## 4 · Feedback Google Form

Create form with 5 fields (overall experience, latency rating, bugs, feature wish, email optional). Copy *share link*.
Add footer link:

```tsx
<a href="https://forms.gle/abc123" target="_blank" rel="noopener" className="hover:underline">Feedback</a>
```

Append separator bullet.

---

## 5 · Compose invite email

`docs/alpha_email.md`:

```md
Subject: 🌱 Gibsey Alpha – Your Invite Code Inside

Hey friend!

Thanks for testing Gibsey. Your one‑time invite code is **$TOKEN**.

1. Go to https://alpha.gibsey.com
2. Click **Sign in** and enter the code + your email.
3. Open the magic‑link in your inbox.

▶️ 3‑min walkthrough video: https://loom.com/share/abcdef
📝 Please drop feedback here: https://forms.gle/abc123

Happy exploring!
– Brennan
```

Use simple mail‑merge in Gmail/SendGrid to inject `$TOKEN` per recipient.

---

## 6 · Track sign‑ups in Airtable/Sheet (optional)

Export `invites` table to CSV daily or hook Supabase webhook to Zapier → Sheet row when `claimed_by` becomes non‑NULL.

---

## 7 · Commit & PR

```bash
git checkout -b day41-alpha-invite
git add docs/alpha_email.md apps/backend/app/routes/invite.py apps/frontend/src/components/SignInModal.tsx
# plus schema migration if committed
git commit -m "feat: invite‑code gate, welcome toast, feedback link"
git push -u origin day41-alpha-invite
```

PR → **Closes #Day-41 issue** → merge when green; move card to **Done**.

---

\### ✅ End‑of‑Day 41 Definition

* Invite table holds 25 tokens; claim API works.
* Sign‑in modal asks for code until claimed.
* Welcome toast & Feedback link live.
* Draft invite email ready for send.

*Tomorrow (Day 42):* run Week‑6 retro, triage alpha feedback, and hotfix anything critical before public tweet.