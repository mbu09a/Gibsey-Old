import { trpc } from '../trpc';

export default function PageDisplay({ pageId }: { pageId: number }) {
  const { data, isLoading, error } = trpc.page.useQuery({ id: pageId });

  if (isLoading) return <p>Loading page...</p>;
  if (error || !data) return <p>Error loading page</p>;

  return (
    <article className="prose prose-invert max-w-none">
      <h2>{data.title ?? 'Untitled'}</h2>
      <p>{data.content}</p>
    </article>
  );
}
