````markdown
# protein-fold.md

## 1. Runtime Overview

Our **Protein-Fold Corpus Interface (PFCI)** uses a **tri-fold state machine**—`READ`, `STORE`, and `EXEC`—to transform symbolic data (here, an SVG snippet) into actionable outputs:

1. **READ** – Interprets the raw symbol content and prepares it for downstream queries.  
2. **STORE** – Retains or updates the symbol’s metadata in a persistent layer.  
3. **EXEC** – Converts the symbol into an operational artifact (e.g., a JSON payload) that can be further processed or executed by external pipelines.

At runtime, a caller selects a state; the system “folds” the symbol accordingly. This folding yields structured data—often JSON—ready for QDPI‑256 or other consuming modules.

---

## 2. Python Stubs

Below is minimal (import‑free) Python code to illustrate how a symbol can be folded based on a given state.  
**Note:** We also show how rotation degrees map to states via a registry.

```python
# protein_fold.py

class CorpusSymbol:
    """
    Represents a symbolic data artifact (e.g., an SVG).
    The fold method transforms content based on tri-fold states.
    """
    def __init__(self, content: str):
        self.content = content

    def fold(self, state: str):
        # Returns a JSON-like dict that QDPI-256 or other modules can consume
        return {
            "state": state,
            "payload": f"Folding content for {state}",
            "source": self.content
        }

# Rotation-to-state registry
ROTATION_REGISTRY = {
    0:   "READ",
    90:  "STORE",
    180: "EXEC",
    270: "READ"
}

if __name__ == "__main__":
    symbol = CorpusSymbol("<svg> ... user-supplied content ... </svg>")
    example_output = symbol.fold("READ")
    print(example_output)
````

**Example Usage**

```bash
python protein_fold.py
# Outputs something like:
# {"state": "READ", "payload": "Folding content for READ", "source": "<svg>...</svg>"}
```

---

## 3. SVG Rotation Spec

When the caller rotates the SVG by a certain angle, the system infers the corresponding tri-fold state:

| Rotation (deg) | Tri-Fold State |
| :------------: | :------------: |
|      **0**     |      READ      |
|     **90**     |      STORE     |
|     **180**    |      EXEC      |
|     **270**    |      READ      |

**Inline SVG Rotation Example**

```html
<svg viewBox="0 0 1000 1000" style="transform: rotate(90deg);">
  <!-- Original symbol elements go here -->
</svg>
```

When rotated to `90deg`, the above snippet implies a `STORE` fold state.

---

## 4. The Symbol (User-Supplied)

```xml
<svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg">
  <!-- White background -->
  <rect width="1000" height="1000" fill="#ffffff"/>
  
  <!-- Top horizontal bar -->
  <line x1="200" y1="200" x2="800" y2="200" stroke="#000000" stroke-width="60" stroke-linecap="square"/>
  
  <!-- Left vertical bar -->
  <line x1="200" y1="200" x2="200" y2="800" stroke="#000000" stroke-width="60" stroke-linecap="square"/>
  
  <!-- Right vertical bar -->
  <line x1="800" y1="200" x2="800" y2="800" stroke="#000000" stroke-width="60" stroke-linecap="square"/>
  
  <!-- Bottom-left foot -->
  <line x1="200" y1="800" x2="400" y2="800" stroke="#000000" stroke-width="60" stroke-linecap="square"/>
  
  <!-- Bottom-right foot -->
  <line x1="800" y1="800" x2="600" y2="800" stroke="#000000" stroke-width="60" stroke-linecap="square"/>
</svg>
```

---

## 5. Integration Notes

1. **QDPI‑256 Pipeline**

   * The `.fold(state)` method returns a JSON-ready dict. This can be ingested by a QDPI‑256 flow for further “query, decode, process, and integrate” operations.

2. **QEE or MNR**

   * After folding, the resulting payload can be piped to **QEE** (Quantum Expression Engine) or **MNR** (Multi-Nodal Runner).
   * Typical usage:

     1. **READ** – Pre-process and classify the symbol for semantic indexing.
     2. **STORE** – Cache or update ledger references for future recall.
     3. **EXEC** – Trigger advanced transformations or initiate real-time data manipulations.

This modular approach lets front-end devs rotate the SVG for UI hints and back-end services interpret those rotations as distinct fold states—tying visual orientation directly to function.

```
```