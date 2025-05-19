import { useState } from "react";
import { ask, saveVault } from "./lib/api";
import VaultTimeline from "./components/VaultTimeline";
import PageDisplay from "./components/PageDisplay";
import Navigation from "./components/Navigation";
import SearchJump from "./components/SearchJump";

export default function App() {
  const [pageId, setPageId] = useState(1);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState<string | null>(null);
  const [loadingQ, setLoadingQ] = useState(false);
  
  const submit = async () => {
    setLoadingQ(true);
    try {
      const resp = await ask(question);
      setAnswer(resp.answer);
    } catch (e) {
      alert((e as Error).message);
    } finally {
      setLoadingQ(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <Navigation pageId={pageId} onChange={setPageId} />
      <SearchJump onJump={setPageId} />

      <PageDisplay pageId={pageId} />

      <div className="space-y-4">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask Gibsey…"
          className="w-full border px-3 py-2 rounded"
        />
        <button
          onClick={submit}
          disabled={loadingQ || !question}
          className="px-4 py-2 bg-emerald-600 text-white rounded disabled:opacity-50"
        >
          {loadingQ ? "Thinking…" : "Ask"}
        </button>
        {answer && (
          <div className="border-l-4 border-emerald-600 pl-4 text-gray-800">
            <p>{answer}</p>
            <button
              onClick={() => saveVault(1, question, answer)}
              className="mt-2 px-3 py-1 bg-amber-600 text-white rounded"
            >
              Save to Vault
            </button>
          </div>
        )}
      </div>
      
      {/* Vault Timeline */}
      <div className="border-t border-gray-200 dark:border-gray-700 pt-10 mt-10">
        <VaultTimeline />
      </div>
    </div>
  );
}