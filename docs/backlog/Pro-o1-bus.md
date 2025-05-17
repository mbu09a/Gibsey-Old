````markdown
# pro-o1-bus.md

Pro-o1-bus is a message transport design for distributing signals with priority weighting and selectable QoS channels.

## Message Envelope

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ProO1BusEnvelope",
  "type": "object",
  "properties": {
    "id":          { "type": "string" },
    "timestamp":   { "type": "string", "format": "date-time" },
    "source":      { "type": "string" },
    "destination": { "type": "string" },
    "channel":     { "type": "string" },
    "priority":    { "type": "number" },
    "payload":     { "type": "object" },
    "trace":       { "type": "array", "items": { "type": "string" } }
  },
  "required": ["id","timestamp","source","destination","channel","priority","payload"]
}
````

## Priority Weighting Formula

$$
\text{PriorityScore} = \alpha\,(\text{user\_attention}) \;+\; \beta\,(\text{nutrient\_score}) \;+\; \gamma\,\bigl(1 - \text{time\_decay}\bigr)
$$

Where $\alpha + \beta + \gamma = 1$. The rationale is to merge user engagement, MNR nutritional value, and reduced weight over time into a single normalized priority.

## TypeScript Interface

```typescript
interface ProO1Message {
  id: string;
  timestamp: string;
  source: string;
  destination: string;
  channel: string;
  priority: number;
  payload: Record<string, unknown>;
  trace?: string[];
}

function routeMessage(msg: ProO1Message): void {
  const userAttention = 0.7;     // placeholder from context
  const nutrientScore = 0.4;     // from MNR
  const timeDecay = 0.2;         // derived from msg age
  const alpha = 0.4, beta = 0.3, gamma = 0.3;

  const priorityScore =
    alpha * userAttention +
    beta * nutrientScore +
    gamma * (1 - timeDecay);

  msg.priority = Math.max(0, Math.min(1, priorityScore));
  // Further routing logic, e.g. push to WebSocket
}
```

## Quality-of-Service Modes

| Mode         | Bandwidth Expectation  | Latency Expectation | Behavior                             |
| ------------ | ---------------------- | ------------------- | ------------------------------------ |
| best\_effort | Up to 1 MB/s typical   | 100–300 ms average  | Drops possible under load            |
| lossless     | Up to 512 KB/s         | 300–500 ms average  | Retries / guaranteed delivery        |
| real\_time   | Up to 2 MB/s burstable | < 50 ms target      | Priority dispatch, minimal buffering |

## Open Questions

1. How do we parameterize alpha, beta, and gamma at runtime?
2. Should timeDecay be a function of absolute or relative timestamps?
3. What is the maximum payload size before we fragment over WebSockets?
4. Do we require encryption or compression on the bus messages?

```
```