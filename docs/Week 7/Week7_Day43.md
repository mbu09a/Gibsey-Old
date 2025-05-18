# Week 7 — Day 43 (Bug‑Bash & Backlog Triage)

> **Target session:** 2 h  **Goal:** sweep through all open GitHub issues and alpha feedback, label severity, merge/close duplicates, and schedule the must‑fix items for this sprint. No feature coding today—just bug hygiene and board hygiene.
>
> **Outcome:** Every issue has a clear severity (`sev1`/`sev2`/`sev3`) and a Week‑7 label or Beta backlog label. Sev‑1 items have a dedicated hot‑fix branch stubbed.

---

## 1 · Pull latest issues & feedback

1. **GitHub Issues:** open **Issues ▸ Filters ▸ is\:open**.
2. **Slack #alpha-feedback:** read through the last 72 h; convert any unlogged bug into a new GitHub issue (use ✨ **Alpha Feedback** template).
3. **Google Form CSV:** download latest → scan for bug reports; raise issues as needed.

---

## 2 · Severity rubric refresh

| Label  | Definition                           | Action window                |
| ------ | ------------------------------------ | ---------------------------- |
| `sev1` | Data loss, auth failure, crash       | Hot‑fix branch → patch today |
| `sev2` | Functional bug but workaround exists | Schedule this week           |
| `sev3` | Cosmetic / low UX friction           | Move to Beta backlog         |

Add or confirm these labels exist in repo.

---

## 3 · Label & deduplicate

For each open ticket:

1. **Read quickly.** If duplicate, comment “Duplicate of #X” and close.
2. Apply one `sev*` label.
3. Apply `week7` if `sev1` or `sev2`; else `post‑mvp`.
4. Add component labels (`frontend`, `backend`, `infra`) for ownership.

Target ratio guideline:

* 0 Sev‑1 (should be none after Day 42 hot fixes)
* ≤ 5 Sev‑2 in Week 7 column
* Unlimited Sev‑3 in backlog

---

## 4 · Update project board

1. Create **“Week 7 – Bug Fixes”** column if not present.
2. Drag all `week7` tickets into column; order by severity > effort.
3. Archive **Alpha Launch** column (if still open).

---

## 5 · Stub hot‑fix branches (if any Sev‑1)

```bash
# example if issue #201 is Sev-1 auth token bug
git checkout -b hotfix/201-auth-token
# commit WIP repro or failing test only
```

Push branch even if empty so CI spins.

---

## 6 · Quick wins checklist

Identify any Sev‑2 with EST ≤ 1 h (typo, missing alt text, small CSS). Add ✅ emoji in issue title to mark “quick win”. You can batch‑fix these tomorrow.

---

## 7 · Communicate status

Post in Slack #alpha-feedback:

> “Bug triage complete: 0 Sev‑1, 3 Sev‑2 scheduled for this week, 8 Sev‑3 in backlog. Thanks testers — keep reports coming!”

---

## 8 · Commit triage log (optional)

Create `docs/triage/2025‑06‑17.md` summarizing counts & notable dupes. Commit:

```bash
git checkout -b day43-bug-bash
git add docs/triage/2025-06-17.md
git commit -m "docs: bug-bash summary for Day 43"
git push -u origin day43-bug-bash
```

PR → **Closes #Day‑43 issue**.

---

### ✅ End‑of‑Day 43 Definition

* All open issues labeled with severity & scope.
* Week‑7 board column populated; Beta backlog started.
* No Sev‑1 bugs unassigned.

*Tomorrow (Day 44):* implement Vault **edit** endpoint & UI modal.