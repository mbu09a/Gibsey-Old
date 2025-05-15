Below is an architected plan for the **Polyphonic Corpus Harmonic Loom (PCHL)**—a generative, multi‑user music engine that translates QDPI events (**Read, Ask, Receive, Save**) and user states into a living, collaborative symphony. The design leverages **pitch‑class transformations**, polyrhythms, concurrency for dozens of simultaneous users, and a real‑time spatial audio pipeline. Magical Bonds and TNA logic further modulate dynamics, unlocking advanced timbral textures.

---

## 1. Pitch‑Class & Polyrhythm Mapping

### 1.1 Corpus‑to‑Music Mapping

Recall that Gibsey’s “Corpus of 16” symbols each has **4 orientations**. This yields **64** unique “musical tokens.” Each token can be mapped to a **(Pitch Class, Mode, Rhythm, Micro‑Tuning Offset)** tuple:

1. **Base Pitch Classes**: We pick 16 distinct pitch classes from a 24‑TET or 12‑TET system plus micro-tuning offsets. For example, in standard 12‑TET, we define a base pitch set:

   $$
   \{C, C\sharp, D, E\flat, E, F, F\sharp, G, A\flat, A, B\flat, B, C', \dots\}
   $$

   We label them $P_0$ through $P_{15}$. Each *symbol* $S_i$ (where $i=0..15$) is assigned one of these pitch classes.

2. **Orientation → Mode**: Each symbol has 4 possible orientations $O_0, O_1, O_2, O_3$. These map to **modal transformations** of the base pitch class. For instance:

   * $O_0$: Ionian (major scale)
   * $O_1$: Aeolian (natural minor)
   * $O_2$: Lydian
   * $O_3$: Phrygian

   Alternatively, you might choose any 4 modes that suit your aesthetic.

3. **Polyrhythm Time Signatures**: We can assign a default time signature or rhythmic pattern to each symbol. For instance:

   * $S_0$ / $O_0$ → 4/4
   * $S_0$ / $O_1$ → 7/8
   * $S_0$ / $O_2$ → 5/4
   * $S_0$ / $O_3$ → 12/8

   Each combination yields a different feel. Or, the system can choose which time signature to use depending on QDPI event states (Read, Ask, etc.).

4. **Micro‑Tuning Offsets**: To introduce a more “colorful” palette, each orientation can push the pitch by a small offset (±10 cents, ±20 cents). For example:

   * $O_0$: +0 cents
   * $O_1$: +15 cents
   * $O_2$: −10 cents
   * $O_3$: +30 cents

   So if the base pitch class is $F$, orientation $O_2$ might produce $F$ − 10 cents, giving a subtle “bend.”

### 1.2 Neo‑Riemannian Moves

To handle chord transitions, we borrow from **Neo‑Riemannian** theory (the classical “P, L, R” transformations). The engine can define a small set of transformations that “rotate” pitch classes or shift them. Examples:

* **Parallel (P)**: Switch from major to minor (Ionian → Aeolian) but keep the same root.
* **Leading‑tone Exchange (L)**: Move one chord tone by a semitone to find a new chord.
* **Relative (R)**: Move from a major chord to its relative minor (C→Am).

By assigning a transformation to each QDPI event, we get real-time chord changes:

| Event            | Transformation                                 |
| ---------------- | ---------------------------------------------- |
| **Read** (R)     | Identity (no change) or simple P (major↔minor) |
| **Ask** (A)      | L or R to modulate tension                     |
| **Receive** (Re) | P + L combined (complex shift)                 |
| **Save** (S)     | R plus a microtonal shift                      |

This ensures that each user’s storyline action updates the harmonic “center” in a consistently shifting, yet coherent way.

---

## 2. Algorithm Pseudocode for Layered MIDI/OSC

Below is a high‑level algorithm that:

1. **Ingests** text embeddings + sentiment vectors from QDPI usage.
2. **Maps** them into layered MIDI or OSC streams.
3. **Supports** concurrency for dozens of simultaneous user threads.

```pseudo
function PCHL_Engine_Step(userActions, userEmbeddings, globalHarmonyState):
    # userActions: array of (userID, QDPIevent, CorpusSymbol, orientation)
    # userEmbeddings: array of (userID -> (textEmbedding, sentiment))
    # globalHarmonyState: store keys, chord centers, etc. for global orchestration

    # 1. Construct a user-level musical context for each action
    for action in userActions:
        userID = action.userID
        symbolIndex = action.CorpusSymbol # 0..15
        orientation = action.orientation  # 0..3
        qdpiEvent = action.QDPIevent     # e.g. "Ask"

        # Retrieve pitch info from mapping
        basePitchClass = BASE_PITCHES[symbolIndex]
        mode = ORIENTATION_MODE_MAP[orientation]
        microOffset = ORIENTATION_MICRO_TUNING[orientation]
        timeSig = ORIENTATION_TIME_SIG[orientation]

        # 2. Factor in sentiment or text embeddings to modulate dynamics / velocity / articulation
        # e.g. sentiment in [-1..+1], textEmbedding might shift chord color
        sentiment = userEmbeddings[userID].sentiment
        dynamicLevel = mapSentimentToDynamic(sentiment) # e.g. range [40..100] for MIDI velocity
        articulation = mapEmbeddingToArticulation(userEmbeddings[userID].textEmbedding)

        # 3. Use a concurrency model for layering
        # Each user gets a "track" or "channel"
        # Possibly group users by similar sentiment or symbol combos to produce parallel harmony

        # 4. Generate or schedule events for MIDI/OSC
        trackID = getOrCreateTrackForUser(userID)
        chordOrNoteSet = applyNeoRiemannianTransform(globalHarmonyState, qdpiEvent)

        # For each note in chordOrNoteSet:
        for note in chordOrNoteSet:
            pitch = combinePitch(note, basePitchClass, microOffset, mode)
            duration = pickDuration(timeSig, userID)
            velocity = dynamicLevel
            articulationParams = articulation

            scheduleNote(trackID, pitch, duration, velocity, articulationParams)

    # 5. Return updated global harmony state
    # e.g. store last chord center for next step
    return updatedGlobalHarmonyState

function scheduleNote(trackID, pitch, duration, velocity, articulation):
    # Implementation for sending MIDI or OSC messages
    # MIDI:
    #   sendMidiMessage(trackID, NOTE_ON, pitch, velocity)
    #   schedule future NOTE_OFF after 'duration'
    # OSC:
    #   oscSend("/pchl/note", [trackID, pitch, velocity, duration, articulation])

    # This is asynchronous so we can handle many user threads
```

### Concurrency Model

* **Each user** is assigned a channel or track in the engine.
* If dozens of users are simultaneously generating events, we layer them in real‑time.
* The engine merges or crossfades chord changes using a global harmony state but can also create local polyrhythms.
* Possibly each user runs in a “goroutine” or “async task,” sending updates to a central scheduling system that dispatches the MIDI/OSC messages in near real‑time.

---

## 3. Spatial‑Audio Pipeline Spec

To place these polyphonic streams into 3D space (AR/VR or physical arrays), we propose:

1. **Front‑End**: **Web Audio API** (for browser) or **native audio engine** (Unity, Unreal, custom).
2. **HOLO‑Binaural Rendering**:

   * Use an HRTF (Head‑Related Transfer Function) library to position each user’s track in 3D space.
   * For VR/AR: Head tracking updates the binaural mix so the user perceives each track in a stable position around them.
3. **Loudspeaker Arrays**:

   * If you have an installation with multiple speakers in a physical environment, apply amplitude panning or wave field synthesis to place each part in the room.
   * Each user track is assigned a 3D coordinate that orbits the listener or dynamically moves (like a rotating sound object).

### Example Setup (Web Audio API + HOLO)

1. **Receive OSC** from the PCHL engine or local scheduling logic.
2. **Instantiate AudioNodes** in the Web Audio API for each user’s track.
3. **Attach a PannerNode** or SpatialPannerNode to each track with **HRTF**.
4. Update positions regularly based on a simple orbit or user location logic.
5. For VR: integrate with the platform’s **headset orientation** so the binaural effect is correct.

---

## 4. Feedback Loop Rules (Magical Bonds & TNA)

### 4.1 Magical Bonds Modulate Dynamics

* **Magical Bond Level**: A measure of trust/connection. High levels = higher volume or more expressive reverb; low levels = subdued parts.
* The engine can check each user’s Magical Bond level before scheduling notes:

  ```pseudo
  if magicalBondLevel(userID) > threshold:
      increaseVolume(trackID, +6 dB)
      addReverb(trackID, "cathedral")
  else:
      decreaseVolume(trackID, -3 dB)
  ```

### 4.2 TNA Unlocking Rare Timbres

* **Time, Need, Access**: If a user invests enough “Time” or meets the “Need” criteria, the system unlocks special instrument patches or “legendary timbres.”
* Example: A user who has saved many shards or participated heavily in QDPI might get a custom “glass harmonica” or “ethereal choir” patch for their parts:

  ```pseudo
  if TNA_condition(userID) == "unlocked":
      setInstrument(trackID, "rare_glass_harmonica")
  ```

This fosters a gift economy approach: the more the user invests (reads, asks, receives, saves), the richer their unique part of the polyphonic tapestry.

---

## 5. Evaluation Metrics

1. **Harmonic Tension Drift**

   * Over time, track the difference between the local chord centers and the global chord center (e.g., a measure of dissonance or tension).
   * Keep it in a target range (say 0–20% tension) to avoid chaotic sound.

2. **Listener Engagement Half‑Life**

   * The average time until a user disengages (closes the app or stops listening).
   * Target an extended half‑life by adjusting variety and tension in the music.

3. **Network Jitter Tolerance < 30 ms**

   * Because we rely on near real‑time concurrency, the system must handle up to 30 ms of variation in message arrivals.
   * We can use local buffering or short term re‑sync if a user’s events arrive late or out of order.

---

## Summary

The **Polyphonic Corpus Harmonic Loom (PCHL)** merges QDPI events with a dynamic musical framework:

* **64 Musical Tokens** (16 symbols × 4 orientations) → **Pitch Classes + Modes + Rhythms + Micro‑Tuning**.
* **Neo‑Riemannian** chord transitions tied to **Read→Ask→Receive→Save** flows, ensuring coherent harmonic narrative.
* **Concurrent** multi‑user layering, orchestrated via **MIDI/OSC** to handle real‑time collaboration.
* **Spatial Audio** with **Web Audio + HOLO** or multi‑speaker arrays to envelop listeners in an interactive, orbiting sound field.
* **Feedback Loops** leveraging Magical Bonds & TNA to scale dynamic levels, timbre unlocks, and overall musical “presence.”
* **Evaluation** of harmonic tension drift, user engagement, and network jitter ensures stable and satisfying generative compositions.

In essence, PCHL transforms every user’s QDPI journey into a living “multi‑user symphony,” weaving ephemeral data and musical structures into an ever‑shifting tapestry of sound.