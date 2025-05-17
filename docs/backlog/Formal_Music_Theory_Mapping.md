# **1. Formal Music-Theory Mapping**

In the Corpus Symphonic Engine (CSE), we align textual symbols and contextual “orientations” (e.g. sentiment polarity, discourse function, semantic domain) with musical keys and transformations. This leverages both modern set theory and Neo‑Riemannian transformations.

## **1.1 Mapping Corpus Symbols to Keys and Modes**

1. **Corpus Symbols**

   * **Letters/Tokens**: e.g. words, punctuation, or special symbols (like `<READ>`, `<ASK>`, `<RECEIVE>`, `<SAVE>`).
   * **Orientation Vectors**: e.g. sentiment (positive ↔ negative), urgency (low ↔ high), or directionality (inward reflection ↔ outward action).

2. **Modal Assignments**

   * **Ionian (Major)**: Aligns with positivity or forward-looking content (e.g., a user’s aspirational text).
   * **Aeolian (Natural Minor)**: Aligns with reflective or somber content (e.g., introspective passages).
   * **Dorian, Phrygian, Lydian, etc.**: Mapped to more nuanced states (e.g., tension, question-asking, transitional states).

3. **Key Selection and Shifts**

   * **Set-Theoretic Anchor**: We treat each mode as a six- to seven-note set (e.g., Ionian = {C, D, E, F, G, A, B}).
   * **Orientation → Transposition**: Orientation vectors produce dynamic key shifts. For example, a strongly positive orientation might transpose Ionian up by a perfect fifth, while a negative orientation might shift Aeolian down by a minor third.

## **1.2 Neo‑Riemannian Transformations**

Neo-Riemannian theory focuses on triadic transformations:

* **L (Leittonwechsel)**: Shifts a major triad to its relative minor or vice versa (e.g., C major → A minor).
* **R (Relative)**: Alters a major triad to another major triad a third away (e.g., C major → E major) or similar.
* **P (Parallel)**: Switches from major to minor on the same root or vice versa (C major → C minor).

In the CSE:

* **Text Polarity** (positive ↔ negative) triggers **P** transformations.
* **Semantic Shift** (topic changes or abrupt transitions) triggers **L** transformations.
* **Forward Narrative Tension** (subtle changes or bridging phrases) triggers **R** transformations.

This mapping ensures that changing textual contexts yield distinct harmonic modulations in real time.

---

# **2. Pseudocode for 100-Word Shard → MIDI**

Below is a high-level pseudocode illustrating how a text shard of \~100 words is analyzed, assigned sentiment vectors, and converted into a stream of MIDI events. The algorithm is simplified for clarity:

```python
function generateMIDIFromTextShard(text_shard):
    # 1. Tokenize the shard
    tokens = tokenize(text_shard)  # e.g., split on whitespace, punctuation

    # 2. Compute sentiment & weighting vectors
    sentiment_values = []
    token_weights = []
    for token in tokens:
        sentiment_score = sentiment_analysis(token)  # range: -1.0 to +1.0
        weight = compute_token_weight(token)         # e.g., freq-based or tf-idf
        sentiment_values.append(sentiment_score)
        token_weights.append(weight)

    # 3. Derive average or cumulative orientation
    overall_sentiment = average(sentiment_values)  # overall shard mood
    total_weight = sum(token_weights)

    # 4. Determine scale/mode based on overall sentiment
    if overall_sentiment > 0.2:
        mode = 'Ionian'
        root_note = 60  # Middle C in MIDI
    elif overall_sentiment < -0.2:
        mode = 'Aeolian'
        root_note = 57  # A below middle C
    else:
        mode = 'Dorian'
        root_note = 62  # D above middle C

    # 5. Map tokens to notes
    # Example: each token maps to a diatonic pitch in the chosen mode
    diatonic_scale = get_scale(mode, root_note)

    midi_events = []
    time_cursor = 0

    for i, token in enumerate(tokens):
        # Weighted velocity and duration
        velocity = clamp(int(token_weights[i] * 100), 1, 127)
        duration = compute_duration(sentiment_values[i], token_weights[i])
        
        # Choose pitch from diatonic scale
        pitch_index = i % len(diatonic_scale)
        pitch = diatonic_scale[pitch_index]
        
        # Add variation if sentiment is negative or positive
        if sentiment_values[i] < -0.5:
            pitch -= 1  # slight downward shift for dissonance
        elif sentiment_values[i] > 0.5:
            pitch += 2  # skip a scale step upward for brightness
        
        midi_events.append({
            'type': 'note_on',
            'pitch': pitch,
            'velocity': velocity,
            'time': time_cursor
        })
        
        # note_off after 'duration' beats
        midi_events.append({
            'type': 'note_off',
            'pitch': pitch,
            'time': time_cursor + duration
        })

        time_cursor += duration
    
    # 6. Return or export MIDI data
    return convert_to_MIDI(midi_events)
```

**Key Points**

* **Sentiment** directly influences **mode** (major vs. minor leaning) and micro-shifts in pitch.
* **Weight** influences **velocity** (dynamics) and **note duration**.
* The final MIDI sequence can be post‑processed (e.g., added chord layering, rests, or additional orchestration rules).

---

# **3. Signal-Flow Diagrams**

The CSE system integrates multiple components for real-time generative music based on textual input. Here is a layered breakdown:

## **3.1 High-Level Architecture**

```
Text Input
   ↓ (tokenization & embedding)
Corpus Symphonic Engine (CSE)
   1. Text Analysis Layer
   2. Embedding Vector Processor
   3. Musical Generator (algorithmic composition + NRT)
   ↓
FastAPI Backend
   ↓
MIDI / Audio Data
   ↓
Web Audio API Frontend
   ↓
Live-Coded Improv Layer (Optional)
   ↓
User Playback & Interaction
```

## **3.2 Detailed Signal Flow**

1. **User/AI Submits Text**

   * Via **FastAPI** endpoint (`POST /corpus`), the text is tokenized and sentiment-analyzed.
   * Embeddings are retrieved (e.g., from a vector database or an on-the-fly embedding model).

2. **CSE Processing**

   * **Text Analysis Layer**: Maps tokens → sentiment/weight vectors.
   * **Embedding Vector Processor**: Calculates dynamic orientation (e.g., expansions, contractions, semantic domain shifts).
   * **Musical Generator**:

     * Chooses mode/key or triadic transformations.
     * Creates MIDI event stream (notes on/off).

3. **API Response**

   * FastAPI returns a JSON payload containing either raw MIDI data (base64-encoded) or a stream of musical instructions (OSC-like, if real-time streaming is needed).

4. **Web Audio API**

   * In the browser, a **Web Audio API** client decodes the musical instructions and renders them.
   * Or a custom front-end synthesizes the notes in real time.

5. **Live-Coded Improv Layer**

   * Performers or advanced users can intercept the MIDI/OSC stream, layering in real-time modifications via a platform like SuperCollider, TidalCycles, or Sonic Pi.
   * This feedback loop can push new instructions back to the CSE, altering the generative output.

---

# **4. Three UX Mock-Scenarios**

Below are example user journeys illustrating how musical modulations guide reading and creativity:

## **4.1 Reflective Poem Reading**

* **Context**: A user opens a poem with introspective and somber language.
* **System Reaction**: CSE identifies negative or melancholy sentiment, chooses Aeolian or Phrygian. The user hears a subdued, minor melody.
* **Outcome**: The quietly shifting triads highlight the “negative space” between lines, nudging the reader to reflect deeper on each phrase’s emotional undertones.

## **4.2 Brainstorming Session in a Collaborative Editor**

* **Context**: Two users are co-editing a text document. As they insert bold or urgent phrases, the system detects an “active” orientation.
* **System Reaction**: Each time a user types an exclamation mark or asks a question, the music modulates from Aeolian to Mixolydian, brightening or adding tension.
* **Outcome**: Musical cues help collaborators sense which parts of the doc are in flux, guiding them to leave “negative space” in the text for future elaboration.

## **4.3 Exploratory Freewriting into Liminal Creativity**

* **Context**: A user enters “liminal mode,” an experimental zone for free association.
* **System Reaction**: The CSE toggles quickly among parallel modes (C Major ↔ C Minor) in response to rapidly shifting word choices. The sonic palette is unsettled, encouraging open-ended thought.
* **Outcome**: The user remains aware of subtle harmonic tensions and resolves them by clarifying or reorganizing ideas. The music’s pushing and pulling fosters that in-between creative state, inviting novel insights.

---

# **5. Property-Based Tests**

To ensure CSE maintains **reversible alignment** between text edits, embedding drift, and harmonic tension, we define property-based tests that randomly generate text changes and verify expected musical outcomes.

## **5.1 Example Test Properties**

1. **Text-Edit → Harmonic Consistency**

   * **Given** a text shard $T$ with a known embedding vector $E$ and resulting chord progression $CP$.
   * **When** we apply a minimal edit $\Delta T$ that slightly changes sentiment or topic.
   * **Then** the new embedding $E'$ and chord progression $CP'$ must differ from $E$ and $CP$ in a bounded manner (e.g., partial chord shifts but not a complete key jump).
   * **And** if we revert $T' = T + \Delta T$ back to $T$, we should revert to the original chord progression $CP$.

2. **Embedding Drift ↔ Dissonance**

   * **Given** a random text generator that produces increasingly divergent semantic fields, measure embedding distance $\| E_i - E_{i+1} \|$.
   * **Check** if the chord progression difference (via a difference function on chords, like a chord distance metric) correlates with the embedding distance.
   * **Property**: Large embedding drifts should lead to more pronounced musical modulations (e.g., a major shift in mode or root note). Small embedding changes only produce local triadic transformations.

3. **Sentiment Polarity ↔ Mode Integrity**

   * **Given** a baseline text with neutral sentiment, cause incremental changes that drive the sentiment from negative to positive.
   * **Check** that the system transitions modes along a plausible path (e.g., Aeolian → Dorian → Ionian).
   * **Property**: No abrupt leaps beyond a one- or two-step transformation unless the text shift is extremely large in semantic or emotional scale.

## **5.2 Execution**

* These tests can be run continuously in a CI pipeline:

  * Generate or mutate text.
  * Compute embeddings and generate MIDI.
  * Inspect the resulting chord/mode transitions.
  * Validate that reversibility and scaling behaviors match expected bounds.

By rigorously verifying the correlation between textual changes, embedding drift, and harmonic tension, the CSE remains stable, expressive, and coherently “in tune” with the evolving corpus.

---

## **Conclusion**

The Corpus Symphonic Engine (CSE) combines formal music-theory mappings (including set-theoretic and Neo‑Riemannian transformations) with sentiment-driven token weighting to transform text shards into a living musical tapestry. By integrating with FastAPI, the Web Audio API, and optional live-coded layers, CSE provides a dynamically modulating audio environment that not only reflects textual content but also inspires creative, liminal reading experiences. The property-based testing strategy ensures reversibility and coherence at every step—keeping the user’s textual intentions and the resulting musical outcomes in harmonious alignment.