import { createTRPCReact } from '@trpc/react-query';
import { httpBatchLink } from '@trpc/client';
import type { AppRouter } from '../server';

export const trpc = createTRPCReact<AppRouter>();

export function createClient() {
  return trpc.createClient({
    links: [
      httpBatchLink({ url: '/trpc' }),
    ],
  });
}
