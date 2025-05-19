import { useState } from 'react';

interface Props {
  onJump: (id: number) => void;
}

export default function SearchJump({ onJump }: Props) {
  const [val, setVal] = useState('');

  return (
    <form
      onSubmit={e => {
        e.preventDefault();
        const id = parseInt(val, 10);
        if (!isNaN(id)) onJump(id);
      }}
      className="flex gap-2"
    >
      <input
        value={val}
        onChange={e => setVal(e.target.value)}
        placeholder="Page #"
        className="px-2 py-1 border flex-1"
      />
      <button type="submit" className="px-3 py-1 border">
        Jump
      </button>
    </form>
  );
}
