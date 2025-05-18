<html><head></head><body><h1>Week 4 — Day 28 (Retro &amp; Week 5 Planning)</h1>
<blockquote>
<p><strong>Target session:</strong> ≈ 1 h  <strong>Goal:</strong> capture Week 4 outcomes, latency/cost data, and prime the board for Week 5 (Auth &amp; RLS). If you still have runway, wire Grafana’s built‑in JSON‑data source to visualize token spend.</p>
<p><strong>Outcome:</strong> <code inline="">README-W4.md</code> retro committed; project board now has a “Week 5&nbsp;– UX Polish + Auth” column with seed issues; optional Grafana dashboard JSON checked in.</p>
</blockquote>
<hr>
<h2>1&nbsp;·&nbsp;Write the Week 4 retrospective</h2>
<p>Create <strong><code inline="">docs/README-W4.md</code></strong> (or append):</p>
<pre><code class="language-md">## Week&nbsp;4&nbsp;Retrospective

### Highlights ✨
- Full 710‑page corpus ingested; count verified 743 total rows.
- Pinecone dual‑store routing dropped P90 latency from 1.8 s → **1.1 s**.
- Bench CI gate prevented regressions—caught a mis‑configured parallelism flag.
- Loading skeleton improved user perception; mobile Lighthouse 95&nbsp;→ 99.

### Friction ↯
- Pinecone client timeouts during first 500‑vector batch (solved by batch=100).
- Embed‑cron cost estimate off by 12&nbsp;% due to forgotten completion tokens.

### Scope tweaks ➰
- Full Grafana cost dashboards moved to optional Stretch.
- RLS/auth still deferred to Week&nbsp;5; no leaks observed.

### Metrics 📊 (last 100 /ask queries)
| Metric | Value |
|--------|-------|
| P50 latency | xxx ms |
| P90 latency | xxx ms |
| Avg cost per ask | $0.00xx |
| Pinecone QPS | x.y |

### Team pulse 💚
- Battery: 4 / 5 – marathon week but no firefights; automation helped.
</code></pre>
<p>Commit:</p>
<pre><code class="language-bash">git add docs/README-W4.md
git commit -m "docs: add Week&nbsp;4 retrospective"
</code></pre>
<hr>
<h2>2&nbsp;·&nbsp;Create Week&nbsp;5 board column &amp; seed issues</h2>
<h3>2.1 New column</h3>
<p>Project board → <strong>Add column</strong> → <strong>“Week&nbsp;5&nbsp;– UX Polish + Auth”</strong>.</p>
<h3>2.2 Seed issues</h3>

Issue Title | Labels
-- | --
Day 29 – Supabase Auth sign‑up / login modal | week5, frontend, auth
Day 30 – API JWT guard + RLS policies on Vault | week5, backend, auth
Day 31 – Passwordless magic‑link email flow | week5, backend, auth
Day 32 – Mobile nav bar & symbol picker polish | week5, frontend, design
Day 33 – Accessibility audit (axe + Lighthouse) | week5, frontend, accessibility
Day 34 – Token & cost dashboard in Grafana | week5, infra, metrics
Day 35 – Sprint retro & Alpha deployment checklist | week5, docs
Drag cards into new column. |  


<hr>
<h2>3&nbsp;·&nbsp;Optional: Grafana dashboard JSON</h2>
<p>If you have Grafana running via Docker Compose:</p>
<ol>
<li>
<p>Create dashboard → panel querying Loki or JSON‑file for token cost.</p>
</li>
<li>
<p>In Grafana → dashboard JSON → <strong>Export</strong> → save as <code inline="">infra/dashboards/cost.json</code>.</p>
</li>
<li>
<p>Add to repo + <code inline="">.grafana/provisioning/dashboards.yaml</code> so it auto‑loads.</p>
</li>
</ol>
<p>Commit (optional):</p>
<pre><code class="language-bash">git add infra/dashboards/cost.json infra/grafana-provisioning.yaml
git commit -m "feat: cost dashboard JSON (optional)"
</code></pre>
<hr>
<h2>4&nbsp;·&nbsp;Push &amp; PR</h2>
<pre><code class="language-bash">git checkout -b day28-retro-week5
git push -u origin day28-retro-week5
</code></pre>
<p>Open PR → <strong>Closes #Day‑28 issue</strong> → merge when green; move Week&nbsp;4 column to <strong>Done</strong> (archive to keep board clean).</p>
<hr>
<h3>✅ End‑of‑Day&nbsp;28 Definition</h3>
<ul>
<li>
<p>Week&nbsp;4 retro committed and merged.</p>
</li>
<li>
<p>Week&nbsp;5 column with issues exists; next sprint ready.</p>
</li>
<li>
<p><em>(Optional)</em> Grafana cost dashboard checked in.</p>
</li>
</ul>
<p><strong>Month‑one core build complete.</strong> Alpha‑launch sprint starts tomorrow with authentication &amp; UX shine! :rocket:</p></body></html>