<html><head></head><body><h1>Week 2 — Day 14 (Sprint Retro&nbsp;&amp; Week 3 Planning)</h1>
<blockquote>
<p><strong>Target session:</strong> ≈ 1 h  <strong>Goal:</strong> capture lessons learned, latency/cost metrics, and set up the Week 3 board. If time remains, scaffold a Redpanda topic + stub Faust consumer.</p>
<p><strong>Outcome:</strong> <code inline="">README-W2.md</code> has a Retro section, a Week 3 project column exists with seed issues, and (optionally) a minimal event‑spine placeholder runs in Docker.</p>
</blockquote>
<hr>
<h2>1&nbsp;·&nbsp;Write the retrospective</h2>
<p>Open <strong><code inline="">docs/README-W2.md</code></strong> (create if absent) and paste this template, then fill it in:</p>
<pre><code class="language-md">## Week&nbsp;2 Retrospective

### What went well?
-
-
-

### What puzzled or slowed us?
-
-

### Scope shifts?
-

### Latency / Cost metrics (average)
| Metric | Value |
|--------|-------|
| /ask latency | xx ms |
| Prompt tokens | xx |
| Completion tokens | xx |
| Cost per /ask | $0.00xx |

### Emotional battery
- Rating: X&nbsp;/&nbsp;5 (brief note)
</code></pre>
<p>Commit:</p>
<pre><code class="language-bash">git add docs/README-W2.md
git commit -m "docs: add Week 2 retrospective"
</code></pre>
<hr>
<h2>2&nbsp;·&nbsp;Set up Week 3 GitHub Project column &amp; issues</h2>
<h3>2.1&nbsp;Create new column</h3>
<ul>
<li>
<p>Open your <strong>Week‑1/2 Project board</strong> → <strong>New column</strong> → name it <strong>“Week&nbsp;3 – Gift Loop &amp; Vault UX”</strong>.</p>
</li>
</ul>
<h3>2.2&nbsp;Seed issues (copy‑paste titles)</h3>

Issue Title | Labels
-- | --
Day 15 – Kafka topic gift_events | week3, infra
Day 16 – Faust consumer persists gifts | week3, backend, infra
Day 17 – Vault UI real‑time updates | week3, frontend
Day 18 – Delete/edit entries endpoint | week3, backend
Day 19 – Symbol chip UI + shadcn button set | week3, frontend
Day 20 – Full Tailwind dark‑mode theme | week3, frontend, design
Day 21 – Sprint retro & Week 4 planning | week3, docs


<p>Drag them to the new column.</p>
<p><em>(Adjust titles/days if you start Week&nbsp;3 on a different calendar date.)</em></p>
<hr>
<h2>3&nbsp;·&nbsp;Optional stub: Redpanda&nbsp;+ Faust</h2>
<h3>3.1&nbsp;Add Redpanda service to <code inline="">infra/compose.yaml</code></h3>
<pre><code class="language-yaml">  kafka:
    image: redpanda/redpanda:v24.1.1
    command: redpanda start --overprovisioned --smp 1 --memory 256M --reserve-memory 0M --node-id 0
    ports:
      - "9092:9092"
</code></pre>
<h3>3.2&nbsp;Create Faust app skeleton <code inline="">apps/backend/app/faust_worker.py</code></h3>
<pre><code class="language-python">import faust
app = faust.App("gibsey-gift", broker="kafka://kafka:9092")

class Gift(faust.Record, serializer="json"):
    page_id: int
    question: str
    answer: str
    ts: float

gifts = app.topic("gift_events", value_type=Gift)

@app.agent(gifts)
async def persist(gift_stream):
    async for gift in gift_stream:
        print("[faust] received", gift)
        # TODO: insert into vault table
</code></pre>
<p><em>(Don’t hook it into <code inline="">/vault/save</code> yet—Week&nbsp;3 task.)</em></p>
<p>Commit stub (optional):</p>
<pre><code class="language-bash">git add infra/compose.yaml apps/backend/app/faust_worker.py
git commit -m "chore: add Redpanda service and Faust stub"
</code></pre>
<hr>
<h2>4&nbsp;·&nbsp;Push&nbsp;&amp; PR</h2>
<pre><code class="language-bash">git checkout -b day14-retro
git push -u origin day14-retro
</code></pre>
<p>Open PR → <strong>Closes #Day‑14 issue</strong> → merge after green CI.<br>
Move the Day&nbsp;14 card to <strong>Done</strong>. Archive Week&nbsp;2 column (optional).</p>
<hr>
<h3>✅ End‑of‑Day&nbsp;14 Definition</h3>
<ul>
<li>
<p>Retro committed in <code inline="">README-W2.md</code>.</p>
</li>
<li>
<p>Week&nbsp;3 column with seed issues on the board.</p>
</li>
<li>
<p><em>(Optional)</em> Redpanda + Faust skeleton merged and running via <code inline="">docker compose up</code>.</p>
</li>
</ul>
<blockquote>
<p><strong>Week&nbsp;2 sprint complete!</strong>  Take a breath and gear up for the Gift Loop &amp; Vault UX sprint.</p>
</blockquote></body></html>