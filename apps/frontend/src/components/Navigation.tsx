interface Props {
  pageId: number;
  onChange: (id: number) => void;
}

export default function Navigation({ pageId, onChange }: Props) {
  return (
    <div className="flex gap-2">
      <button onClick={() => onChange(pageId - 1)} className="px-2 py-1 border" disabled={pageId <= 1}>
        Prev
      </button>
      <button onClick={() => onChange(pageId + 1)} className="px-2 py-1 border">
        Next
      </button>
    </div>
  );
}
