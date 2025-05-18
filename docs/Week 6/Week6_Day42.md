# Week 6 — Day 42 (Retro & Hot‑Fix Triage)

> **Target session:** 1–2 h  **Goal:** wrap the 6‑week MVP marathon with a structured retrospective, review first‑day alpha feedback, and patch any Sev‑1 bugs before the public tweet. Tag `v0.1.1-alpha` with fixes and confirm deploy pipelines fire cleanly.
>
> **Outcome:** `README-W6.md` retro committed; critical issues either fixed or scheduled; project board archived in favor of “Post‑MVP” column. Alpha site stable, latency SLA still < 2 s.

---

## 1 · Collect alpha feedback

* Check Slack #alpha-feedback for bug reports.
* Export Google Form responses → CSV → scan for severity.
* Summarize top 5 pain points in `docs/alpha_feedback.md`.

Severity rubric:

| Level     | Definition                          | Action         |
| --------- | ----------------------------------- | -------------- |
| **Sev‑1** | Data loss, auth failure, blank page | Hot‑fix today  |
| **Sev‑2** | Visual glitch, still functional     | Patch next tag |
| **Sev‑3** | Minor UX nit / feature request      | Log in backlog |

---

## 2 · Patch Sev‑1 bugs

1. Create branch `hotfix/sev1-<slug>` for each critical.
2. Unit test reproduces issue → fix → bump version in `apps/backend/__init__.py` or front‑end `package.json`.
3. Tag & push `v0.1.1-alpha` (or `.2` etc.) → verify **deploy-api** / **deploy-frontend** workflows succeed.
4. Post Slack note: “Patch deployed – please retry.”

---

## 3 · Week‑6 retrospective

Create **`docs/README-W6.md`**:

```md
## Week 6 Retrospective (Alpha Launch)

### Highlights 🎉
- Front‑end + API auto‑deploy tags worked first try (rolling update < 10 s).
- 18/25 testers onboarded within 12 h; zero auth failures.
- UptimeRobot reported 100 % availability.

### Surprises 🤯
- One user hit 1.9 s latency edge‑case (Sydney); Geo edge caching idea.
- Invite code copy/paste confusion (lowercase accepted but modal uppercases). Fixed.

### Metrics 📈 (first 24 h)
| Metric | Value |
|--------|-------|
| Unique users | 18 |
| /ask median | xxx ms |
| /ask P95 | xxx ms |
| OpenAI cost | $0.32 |

### Next‑step themes ➡️
1. **Delete/edit Vault** (top request).
2. **Symbol trail visualisation** desire (already post‑MVP).
3. Add GitHub social login.
```

Commit:

```bash
git add docs/alpha_feedback.md docs/README-W6.md
git commit -m "docs: week‑6 retro + alpha feedback summary"
```

---

## 4 · Archive project board & open Post‑MVP column

* Close **Week 6 – Alpha Launch** column.
* Create new column **Post‑MVP Backlog**; move Sev‑2 & Sev‑3 cards there.
* Label feature ideas with `post-mvp`.

---

## 5 · Tweet / announcement (optional)

Draft tweet in `docs/announcement.md`:

```md
✨ Gibsey alpha is live! Read → Ask → Receive → Save narrative shards in under 2 s. Thanks to our first 25 testers for blazing the trail. Join the waitlist ➡️ gibsey.com 🚀
```

Schedule via TweetDeck or Buffer.

---

## 6 · Commit final docs & PR

```bash
git checkout -b day42-retro-hotfix
git add docs/README-W6.md docs/alpha_feedback.md docs/announcement.md
# plus any hot‑fix code commits
git commit -m "docs: week‑6 retro & hot‑fix tag v0.1.1-alpha"
git push -u origin day42-retro-hotfix
```

PR → **Closes #Day‑42 issue** → merge when green.
Move card to **Done**. Celebrate 🍾.

---

### ✅ End‑of‑Day 42 Definition

* Week‑6 retro merged; Sev‑1 bugs patched & deployed.
* Alpha site stable, feedback consolidated.
* Board archived; Post‑MVP backlog seeded.

**MVP journey complete – on to iterative improvement!**