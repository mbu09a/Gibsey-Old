import express from 'express';
import { initTRPC } from '@trpc/server';
import { createExpressMiddleware } from '@trpc/server/adapters/express';
import fetch from 'node-fetch';
import { z } from 'zod';

const t = initTRPC.create();

const appRouter = t.router({
  page: t.procedure.input(z.object({ id: z.number() })).query(async ({ input }) => {
    const base = process.env.API_BASE || 'http://localhost:8000';
    const r = await fetch(`${base}/read?id=${input.id}`);
    if (!r.ok) throw new Error('failed to fetch page');
    return r.json();
  }),
  section: t.procedure.input(z.object({ pageId: z.number() })).query(async ({ input }) => {
    const base = process.env.API_BASE || 'http://localhost:8000';
    const r = await fetch(`${base}/sections?page_id=${input.pageId}`);
    if (!r.ok) throw new Error('failed to fetch sections');
    return r.json();
  }),
  symbol: t.procedure.input(z.object({ id: z.number() })).query(async ({ input }) => {
    const base = process.env.API_BASE || 'http://localhost:8000';
    const r = await fetch(`${base}/symbol?id=${input.id}`);
    if (!r.ok) throw new Error('failed to fetch symbol');
    return r.json();
  }),
});

export type AppRouter = typeof appRouter;

const app = express();
app.use('/trpc', createExpressMiddleware({ router: appRouter }));

const port = Number(process.env.PORT || 4000);
app.listen(port, () => {
  console.log(`tRPC server listening on port ${port}`);
});
