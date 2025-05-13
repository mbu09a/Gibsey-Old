export async function readPage(id: number) {
  const base = import.meta.env.VITE_API_BASE;
  const r = await fetch(`${base}/read?id=${id}`);
  if (!r.ok) throw new Error("Failed to fetch shard");
  return r.json();
}