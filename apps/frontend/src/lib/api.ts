export async function readPage(id: number) {
  const base = import.meta.env.VITE_API_BASE;
  const r = await fetch(`${base}/read?id=${id}`);
  if (!r.ok) throw new Error("Failed to fetch shard");
  return r.json();
}

export async function ask(question: string) {
  const base = import.meta.env.VITE_API_BASE;
  const t0 = performance.now();
  const r = await fetch(`${base}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, page_id: 1 }),
  });
  const json = await r.json();
  const t1 = performance.now();
  console.log(`🕒 /ask round‑trip: ${Math.round(t1 - t0)} ms`);
  return json;
}