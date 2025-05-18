# Week 7 — Day 49 (Sprint Retro & Beta Go/No-Go)

> **Target session:** 1–2 h  **Goal:** finalize Week‑7 retrospective, close out Sev‑2 tickets, and decide whether the platform is stable enough to invite the full beta wait‑list. Output a concise Go/No‑Go decision document and burn‑down chart.
>
> **Outcome:** `README‑W7.md` retro merged; Sev‑2 bug count zero; Go or No‑Go decision logged in `docs/beta_go_no_go.md`. Project board archived and new “Beta Sprint 1” column seeded.

---

## 1 · Burn down Sev‑2 fixes

1. Filter GitHub issues: `label:sev2 is:open`.
2. For each:

   * If fix committed: close.
   * If still open but trivial (< 30 min): patch now, tag `v0.1.3-alpha`.
   * If non‑trivial: re‑label `sev3` and move to Beta backlog.
     Goal: **0 Sev‑2 open**.

---

## 2 · Week‑7 retrospective

Create **`docs/README‑W7.md`**:

```md
## Week 7 Retrospective (Hardening + Quick Wins)

### Highlights 🌈
- Vault edit/delete live with undo + audit.
- 16‑symbol trails deliver rich UI with zero latency regress.
- Beta wait‑list collected 120 sign‑ups in 18 h.

### Lowlights 🥵
- Pinecone filter bug cost 0.4 s until cache fix.
- Turnstile iframe blocked on Brave w/ shields‑up.

### Metrics (post‑MVP) 📊
| Metric | Value |
|--------|-------|
| Active users last 7 d | 31 |
| /ask P90 (global) | xxx ms |
| OpenAI cost / user / day | $0.011 |

### Team pulse 🔋
Energy 4/5—steady, ready for broader beta.
```

Commit:

```bash
git add docs/README-W7.md
```

---

## 3 · Go/No‑Go decision doc

Create **`docs/beta_go_no_go.md`**:

```md
# Beta Expansion – Go/No‑Go (2025‑06‑23)

**Checklist**
- [x] 0 Sev‑2+ bugs open
- [x] P90 latency < 2 s w/ symbol filter
- [x] Cost / user / day < $0.02 target
- [x] Monitoring alert noise < 2 / wk
- [ ] Counsel review on updated Privacy & TOS (due 06‑28)

**Decision:** **GO** – Invite next 500 wait‑list emails on 2025‑06‑24.

*Risks*
1. Increased vector traffic could bump Pinecone quota—plan upgrade.
2. Turnstile blocking on stricter browsers—fallback hCaptcha if reports spike.
```

Mark **GO** or **NO‑GO** after discussion.

---

## 4 · Update project board

1. Archive **Week 7 – Bug Fixes** column.
2. Create **Beta Sprint 1** column with three starter cards: *Wait‑list invite mailer*, *Turnstile fallback*, *Pinecone quota watch*.

---

## 5 · Burn‑down chart (optional)

If using GitHub Projects insights, screenshot burn‑down; else quick Python plot of sev‑2 count over days. Save to `docs/img/week7_burndown.png` via `python_user_visible` if desired.

---

## 6 · Commit & PR

```bash
git checkout -b day49-retro-go
# add docs, close issues
git commit -m "docs: week‑7 retro & beta go/no-go decision"
git push -u origin day49-retro-go
```

PR → **Closes #Day‑49 issue** → merge when green. Celebrate – 7‑week MVP+, GO for Beta! 🎉

---

### ✅ End‑of‑Day 49 Definition

* Week‑7 retro merged; Sev‑2 bugs zero.
* Beta Go/No‑Go document committed; decision recorded.
* Board transitioned to Beta phase.

**MVP hardening complete – onward to Beta expansion!**