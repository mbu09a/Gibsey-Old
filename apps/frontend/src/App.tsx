import { useState } from "react";
import { readPage } from "./lib/api";

function App() {
  const [page, setPage] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);
  
  const load = async () => {
    setLoading(true);
    try {
      const data = await readPage(1);
      setPage(data);
    } catch (e) {
      alert((e as Error).message);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6 text-gray-800">
      <button
        onClick={load}
        className="mb-4 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50"
        disabled={loading}
      >
        {loading ? "Loading…" : "Fetch Shard"}
      </button>
      {page && (
        <article className="prose lg:prose-xl max-w-none">
          <h2>{page.title}</h2>
          <p>{page.content}</p>
        </article>
      )}
    </div>
  );
}

export default App;