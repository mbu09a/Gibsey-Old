# Sprint‑Zero Data‑Flow Diagram (Author’s Preface Pressure‑Test)

> ASCII first; export to Figma after endpoints stabilize.

```
┌───────────────┐      1.ReadShard         2.Diffuse             3.Recs            4.Save
│   Browser/    │ ─────────────────► ┌─────────────┐ ─────────────────► ┌─────────────┐
│   React UI    │                    │  API GW     │                    │   MNR svc    │
└───────────────┘ ◄────────────────── └─────────────┘ ◄───────────────── └─────────────┘
      ▲  ▲  ▲                               ▲  ▲                                 ▲   |
      │  │  │                               │  │                                 │   │ 5.Ack
      │  │  │                               │  │ 2a.GraphQuery                    │   │
      │  │  │                               │  │                                 │   ▼
      │  │  │                               │  │                        ┌─────────────────┐
      │  │  │                               │  └────────────────────────│  Postgres +     │
      │  │  │                               │                           │  pgvector       │
      │  │  │                               │                           └─────────────────┘
      │  │  │                               │                                  ▲
      │  │  │                               │                                  │ 3b.Top‑N
      │  │  │                               │                                  │
      │  │  │      4a.VaultSave             │                                  │
      │  │  └───────────────────────────────┘                                  │
      │  │                                  ▲                                  │
      │  │                                  │                                  │
      │  │                                  │                                  │
      │  │                        ┌─────────┴─────────┐                        │
      │  │                        │  Vault Service    │ ◄──────────────┐       │
      │  │                        └─────────┬─────────┘                │       │
      │  │                                  │ 4b.Insert                │       │
      │  │                                  ▼                          │       │
      │  │                        ┌─────────────────┐                  │       │
      │  └────────────────────────│  Vault Table    │──────────────────┘       │
      │                           └─────────────────┘                          │
      │                                                                        │
      └─────────────────────────────────────────────────────────────────────────┘
                           6.pro‑o1 Bus (amplify & route all messages)
```

## Legend

1. **ReadShard** → UI fetches shard via `GET /shards/:id`.
2. **Diffuse** → UI POSTs to `/mnr/diffuse`; API Gateway forwards to MNR Service.
3. **Recs** → MNR returns enriched shard list; passed back to UI.
4. **Save** → UI POSTs Vault entry; Vault Service writes to Vault Table and acks UI.
5. **Ack** → Vault Service confirmation.
6. Every request/response is encapsulated in a **pro o1** message envelope and rides the bus.

## Components & Responsibilities

| Node                            | Role                                                                  |
| ------------------------------- | --------------------------------------------------------------------- |
| **Browser/React UI**            | Renders shards, calls APIs, displays recommendations.                 |
| **API Gateway (QDPI‑256 edge)** | Auth, rate‑limit, converts HTTP ↔ pro o1 envelopes.                   |
| **MNR Service**                 | Runs nutrient diffusion graph algorithm.                              |
| **Postgres + pgvector**         | Stores `shards_author_preface` & vector embeddings.                   |
| **Vault Service**               | Persists user‑saved entries; feeds analytics.                         |
| **Vault Table**                 | Partitioned by `user_id`; timeline store.                             |
| **pro o1 Bus**                  | In‑memory (Redis Streams) channel amplifying & routing every message. |

## TODO (for Figma rendition)

* Replace ASCII with swim‑lane diagram.
* Add latency annotations per edge.
* Color‑code internal vs. external calls.

*End of diagram.*