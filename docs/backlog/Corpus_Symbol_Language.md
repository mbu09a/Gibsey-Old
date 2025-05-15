Below is a **reference specification** for the fictional “Corpus Symbol Language” (CSL). It is broken down into the five requested sections. All code/configuration snippets are in fenced code blocks for immediate copy‑paste.

---

## 1. **Concise Grammar (EBNF)**

We will define an EBNF grammar that models:

1. A set of **16 distinct symbols** (named `S0` through `S15`, for example).
2. Each symbol may have **4 orientations** (0°, 90°, 180°, 270°).
3. **Transitions** between symbols can be represented by arrows (e.g., `->` or `~>`).
4. Each symbol–orientation pair maps to an **operational state** in `{Read, Ask, Receive, Save}` (noted but not fully enumerated in the grammar).

### EBNF

```ebnf
CSLDocument       = CSLStatement { ";" CSLStatement } ;

CSLStatement      = SymbolOrientation
                    { TransformationOp SymbolOrientation } ;

SymbolOrientation = SymbolName ":" Orientation ;
SymbolName        = "S0" | "S1" | "S2" | "S3" | "S4"
                  | "S5" | "S6" | "S7" | "S8" | "S9"
                  | "S10"| "S11"| "S12"| "S13"| "S14"| "S15" ;

Orientation       = "0" | "90" | "180" | "270" ;

TransformationOp  = "->" | "~>" | "=>" ;
```

* **CSLDocument** consists of one or more **CSLStatement** separated by semicolons.
* A **CSLStatement** is a sequence of **SymbolOrientation** tokens possibly linked by a transformation operator.
* Each **SymbolOrientation** is a single symbol plus an orientation, e.g. `S3:90`.
* The example transformation operators `->`, `~>`, and `=>` can be extended or specialized.

> **Note:** The grammar describes valid *syntactic* constructs. The *operational state* (`Read`, `Ask`, `Receive`, `Save`) is an implied mapping from `(SymbolName, Orientation)` to a state. The grammar does not prevent collisions in state, but we can define the mapping as a separate table or function.

---

## 2. **Algorithm (Pseudocode) for Converting a CSL String into a Vector‑Embedding Index Key**

We assume:

* Each of the 16 symbols can be indexed from `0..15`.
* Each orientation is indexed from `0..3` (representing {0°, 90°, 180°, 270°}).
* Concatenate them into a single integer index or a vector of integers.

A straightforward approach is:

1. Parse the CSL input string into tokens of `(symbolIndex, orientationIndex)`.
2. For each `(symbolIndex, orientationIndex)` pair, compute a unique integer:

   $$
   \text{uniqueID} = 4 \times \text{symbolIndex} + \text{orientationIndex}.
   $$

   This yields a value from `0..63`.
3. Append these `uniqueID`s to create a final **vector-embedding index key**.

Here is a reference pseudocode:

```pseudo
FUNCTION parseCSL(cslString):
    # Split statements by ';'
    statements = split(cslString, ";")
    
    resultList = []

    FOR each statement in statements:
        # Example token pattern: S3:180 or S7:90, possibly with transformations
        tokens = tokenizeByWhitespaceAndArrows(statement)

        FOR each token in tokens:
            if matchesSymbolOrientationPattern(token):
                (symbolName, orientation) = splitByColon(token)  # e.g. "S3", "180"
                symbolIndex = extractNumber(symbolName)          # e.g. "S3" -> 3
                orientationIndex = orientationToIndex(orientation) 
                    # "0" -> 0, "90" -> 1, "180" -> 2, "270" -> 3

                uniqueID = symbolIndex * 4 + orientationIndex
                append uniqueID to resultList
    
    RETURN resultList


FUNCTION orientationToIndex(orientationString):
    if orientationString == "0":   return 0
    if orientationString == "90":  return 1
    if orientationString == "180": return 2
    if orientationString == "270": return 3


# Example final usage:
# cslString = "S0:0 -> S1:90 ; S10:270 => S3:180"
# embeddingIndexKey = parseCSL(cslString)
# embeddingIndexKey might look like [0, 1*4+1, 10*4+3, 3*4+2] = [0, 5, 43, 14]
```

* `parseCSL` returns a list of **integer indices** corresponding to each `(symbol, orientation)` encountered in the order they appear.
* You can use that list directly or further transform it (e.g., to a dimension‑64 one‑hot vector, or a dimension large enough to hold the entire sequence, etc.).

---

## 3. **UI/UX Interaction Rules**

These rules describe how users (and your React app) interact with:

1. **Symbol Rotation**
2. **Coloring Chat Threads** based on operational state.

### 3.1 Symbol Rotation

* **Tap or Click**:

  * A single click/tap on a symbol cycles through its next orientation in the sequence `(0°, 90°, 180°, 270°, back to 0°)`.
* **Keyboard Shortcut** (optional):

  * Holding `Ctrl + R` (or `Cmd + R`) while clicking increments orientation by +90°.
* **Touch/Drag** (mobile):

  * A short vertical drag rotates the symbol 180°.
  * A short horizontal drag rotates the symbol 90° (left drag is ‑90°, right drag is +90°).

### 3.2 Coloring Chat Threads

Each `(symbol, orientation)` resolves to one of four operational states:

| Orientation Index | State   | Suggested Color  |
| ----------------- | ------- | ---------------- |
| 0 (0°)            | Read    | #8bc34a (Green)  |
| 1 (90°)           | Ask     | #ffc107 (Amber)  |
| 2 (180°)          | Receive | #03a9f4 (Blue)   |
| 3 (270°)          | Save    | #9c27b0 (Purple) |

**Implementation in React**:

* When a symbol is rendered, store the orientation in component state, e.g. `orientationState`.
* The **background color** or **border color** for the chat bubble is derived by mapping `orientationState` to the color table above.
* The symbol’s **icon** or **rotated graphic** is displayed based on `orientationState`.

**Context**:

* Maintain a `CSLContext` with a `dispatch` function to handle **rotateSymbol(symbolId)** actions.
* Each chat “thread” or “bubble” can be wrapped in `<CSLConsumer>` or a custom hook to retrieve the color from the orientation state.

---

## 4. **Example User Flows**

Below are three example flows illustrating:

1. **Negative‑Space Reading**: Where certain symbols (or transformations) are intentionally omitted or read as “gaps.”
2. **Liminal Generativity**: A transitional state that emerges when rotating symbols or changing orientation between recognized states.

### 4.1 **Simple Q\&A Flow (with Negative-Space)**

1. **User Drags** symbol `S0:0` (“Read”) downward to `S0:180` (“Receive”).
2. The UI highlights an **empty** placeholder symbol after that transition, effectively a negative space (no text, no shape).
3. The user chooses not to fill the negative space and moves on, reading it as “unanswered.”
4. The final expression is `S0:180 ~> [  ] ~> S1:90`, where `[  ]` is negative space.
5. The system “reads” that negative space as a silent pause, generating a prompt for the user to “explain the gap.”

### 4.2 **Symbolic Brainstorm Flow (Liminal Generativity)**

1. The user has a sequence: `S5:270 => S7:0 => S7:90`.
2. Each time the user toggles orientation from `270° -> 0°`, a color change from Purple (Save) to Green (Read) prompts the user with an “Input Thought” field.
3. The user types an idea. The symbol then **auto‑rotates** from `S7:0` (Read) to `S7:90` (Ask).
4. This intermediate step between “Read” and “Ask” is a **liminal** transition that the system stylizes with a faint overlay, encouraging the user to reflect on what’s in between reading and asking.

### 4.3 **Collaborative Document Flow**

1. Two participants each manipulate distinct symbols in a shared chat.
2. One participant rotates `S12:0 -> S12:90` to indicate a question (“Ask”).
3. The other participant sees the new orientation color (amber), types a response, and rotates that same symbol to `S12:180` (“Receive”).
4. The partial expression might read `S12:90 -> S12:180`, showing how a single symbol’s orientation changes the conversation.
5. Negative space arises if a participant **skips** a symbol, e.g., leaving `S12:270` out of sequence, which can later lead to generative prompts about “what might have been saved.”

---

## 5. **Property‑Based Tests**

Below are tests to ensure **reversible mapping** between UI state and the CSL expression:

```pseudo
TEST "Parsing and Re-Rendering is Reversible":
    # For randomly generated valid CSL strings
    # 1) parseCSL -> get embeddingIndexKey
    # 2) Re-render UI from that embeddingIndexKey
    # 3) Capture newCSLString from re-render
    # 4) parseCSL(newCSLString)
    # The two embeddingIndexKeys must match

    propertyTest(numTrials = 1000):
        for i in 1..numTrials:
            originalCSL = generateRandomCSLString()  # Must obey grammar
            originalKey = parseCSL(originalCSL)

            # imagine a round-trip: from embeddingKey back to UI -> produce new CSL
            renderedCSL = renderUIToCSL(originalKey)
            roundTripKey = parseCSL(renderedCSL)

            assertEqual(originalKey, roundTripKey)


TEST "UI Orientation and Color are Consistent with Symbol Mappings":
    # For each orientation state in {0, 90, 180, 270}, ensure the color matches {Green, Amber, Blue, Purple}
    # This ensures the UI color logic is invertible and consistent.

    for orientation in [0, 90, 180, 270]:
        color = orientationToColor(orientation)
        # orientationToColor is the function used by the UI to color chat threads
        # Now invert the color or compare with the known table
        assert isCorrectColor(orientation, color)

```

### Explanation

* **Parsing and Re-Rendering is Reversible**
  Confirms that if you parse a random valid CSL string into its internal representation (or “embeddingIndexKey”), then re‑render back into a CSL string, that newly generated string will produce the **same** internal representation when parsed again.

* **UI Orientation and Color**
  Ensures no orientation is assigned the wrong color. This also helps confirm that flipping orientation in the UI is consistent with the grammar’s notion of symbol states.

---

### Putting It All Together

* **Grammar**: Defines the building blocks of CSL syntax.
* **Algorithm**: Converts any CSL expression into a list (or vector) of integer indices.
* **UI/UX Rules**: Guides React component wiring, orientation changes, and color mappings.
* **User Flows**: Illustrate how negative-space reading and liminal states can appear in practice.
* **Tests**: Validate round-trip consistency and orientation→color correctness.

All the components above provide a **blueprint** for implementing the **Corpus Symbol Language** inside a collaborative chat or knowledge system.