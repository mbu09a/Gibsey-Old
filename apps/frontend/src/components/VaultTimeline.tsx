import { useEffect, useState } from "react";
import { MessageSquare, Clock } from "lucide-react";

interface VaultEntry {
  id: number;
  question: string;
  answer: string;
  created_at: string;
}

export default function VaultTimeline() {
  const [entries, setEntries] = useState<VaultEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchEntries = async () => {
      try {
        setLoading(true);
        const response = await fetch(
          `/api/vault/list?limit=20`
        );
        
        if (!response.ok) {
          throw new Error(`Error: ${response.status}`);
        }
        
        const data = await response.json();
        setEntries(data);
        setError(null);
      } catch (err) {
        console.error("Failed to fetch vault entries:", err);
        setError("Failed to load vault entries. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    fetchEntries();
  }, []);

  if (loading) {
    return (
      <div className="mt-8 text-center text-gray-500">
        Loading vault entries...
      </div>
    );
  }

  if (error) {
    return (
      <div className="mt-8 p-4 bg-red-50 text-red-700 rounded-md">
        {error}
      </div>
    );
  }

  if (entries.length === 0) {
    return (
      <div className="mt-8 text-center text-gray-500">
        No entries found in the vault yet.
      </div>
    );
  }

  return (
    <div className="mt-10 space-y-6 max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
        Saved Q&A Entries
      </h2>
      
      <div className="space-y-6">
        {entries.map((entry) => (
          <div 
            key={entry.id} 
            className="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700"
          >
            <div className="flex items-start gap-4">
              <div className="flex-shrink-0 p-2 bg-blue-100 dark:bg-blue-900/30 rounded-full text-blue-600 dark:text-blue-400">
                <MessageSquare className="h-5 w-5" />
              </div>
              
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400 mb-1">
                  <Clock className="h-4 w-4" />
                  <span>
                    {new Date(entry.created_at).toLocaleString(undefined, {
                      dateStyle: 'medium',
                      timeStyle: 'short',
                    })}
                  </span>
                </div>
                
                <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                  {entry.question}
                </h3>
                
                <div className="prose dark:prose-invert max-w-none text-gray-600 dark:text-gray-300">
                  <p className="whitespace-pre-line">{entry.answer}</p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
