Below is a high-level description of the **protocol handshake** that governs how a user’s **shard** (i.e., a discrete data artifact) is transferred from the **CCML** (Convergent Cryptographic Memory Layer) to the **Oneiric Lattice Confluence** (an advanced data-manifold environment). The protocol ensures version integrity, validates provenance, and provides hooks for rolling back if issues arise.

---

## 1. Conceptual Overview

1. **Goal**

   * Securely pass a shard—an encrypted or partially signed data block—from CCML to the Oneiric Lattice.
   * Maintain robust proof-of-origin and ongoing version tracking.
   * Allow for safe reversion in the event of corruption or mismatch.

2. **Core Entities**

   * **CCML Node**: The local system or cluster that manages cryptographic shards.
   * **Confluence Edge**: The gateway to the Oneiric Lattice. Acts as the initial receiver and orchestrator for the handshake.
   * **Lattice Registry**: The authoritative ledger within the Oneiric Lattice that maintains the canonical references (versioning, provenance logs).

3. **Key Objectives**

   * **Versioning**: Tag each shard with a semantically meaningful version ID (e.g., `Major.Minor.Patch` or a cryptographic hash-based index).
   * **Provenance Proofs**: Guarantee the shard’s authenticity and lineage via cryptographic signatures, reference checks, and chain-of-custody records.
   * **Rollback Hooks**: Provide a well-defined mechanism to revert or invalidate a shard’s new state if acceptance into the Lattice fails or if the user triggers an undo event.

---

## 2. Handshake Phases

The transfer process typically unfolds across four distinct phases:

### 2.1 Initialization & Capability Negotiation

1. **Client-Server Hello**

   * **CCML Node** sends a “Hello” message to the **Confluence Edge**, indicating it wishes to transfer a shard.
   * The message includes:

     * **Supported Protocol Versions** (e.g., `v2.0`, `v2.1`, etc.).
     * **Shard Manifest** (a minimal descriptor of the shard’s type, size, intended usage).
     * A ephemeral session key or a reference to the key exchange mechanism in use.

2. **Confluence Edge Response**

   * The **Edge** picks the highest mutually supported protocol version and returns a “Hello-Ack” containing:

     * **Chosen Protocol Version**
     * **Session Token** that will be used for subsequent communication.
   * If versions are incompatible, the handshake terminates gracefully.

### 2.2 Provenance Verification & Authentication

1. **Shard Header & Proof Delivery**

   * The CCML Node sends the shard header, which includes:

     * **Version ID**: A structured or hash-based version reference.
     * **Provenance Chain**: A cryptographic link that references prior versions in the CCML ledger.
     * **Signature Bundle**: Digital signatures from prior signers (e.g., the user’s identity or designated authority).
   * This data is accompanied by a short-living **Authentication Token** (signed with the user’s private key or a CCML master key).

2. **Confluence Edge Verification**

   * Validates the authenticity and integrity of the shard’s header. Checks that:

     * The signature bundle matches known public keys or trust anchors.
     * The declared version does not conflict with an existing entry in the Oneiric Lattice Registry.
   * If any verification fails, the Edge halts further processing and issues an error response.

### 2.3 Payload Transfer & Versioning Commit

1. **Shard Payload Upload**

   * On successful provenance check, the CCML Node streams the shard’s encrypted payload to the **Edge**.
   * The payload is typically broken into smaller chunks for reliability. Each chunk is appended with a micro-signature or Merkle-based integrity proof.

2. **Confluence Edge Assembly**

   * The Edge reconstructs the full shard from the chunks, verifying each piece against the shard header’s hash tree.
   * Once complete, the Edge calculates or confirms the final cryptographic hash to ensure consistency with the declared version ID.

3. **Lattice Registry Commit**

   * The Edge writes a new entry to the **Lattice Registry**, capturing:

     * **Shard Hash** (final integrity check).
     * **Version ID** (aligned with the CCML’s notation).
     * **Provenance Artifacts** (the proof-of-origin references).
     * **Timestamp** of insertion.
     * **Previous Version Link** if this shard supersedes a prior version in the Lattice.
   * If the registry commit is successful, the Edge returns a final “Commit-Ack” to the CCML Node.

### 2.4 Rollback & Reversion Hooks

1. **Rollback Trigger**

   * May occur if the Oneiric Lattice detects an unrecoverable mismatch, or if the user (or an automated policy) requests a revert.
   * The Edge signals a “Rollback-Intent” to the CCML Node, referencing the shard’s version ID and the reason.

2. **Reversion Execution**

   * The Lattice Registry flags the newly inserted shard version as **invalid** or **inactive** (without deleting it, for audit reasons).
   * The prior valid version’s reference is reinstated as the canonical shard in the Lattice, preserving continuity.
   * Optionally, the CCML can remove local references or revert to a previous state if needed. (Often, CCML’s version control remains independent, but the handshake can coordinate synchronization.)

3. **Audit Trail**

   * Both the CCML Node and the Oneiric Lattice preserve logs of the rollback event, including the impetus and final state.
   * Future attempts to reference the invalidated version must pass through a strict override process.

---

## 3. Protocol Artifacts & Data Fields

1. **Shard Manifest**

   * **Type**: e.g., text-based record, binary data, partial script, etc.
   * **Size**: for resource allocation.
   * **Dependencies**: references to other shards or external services.

2. **Provenance Chain**

   * A list of cryptographic hashes or references linking back to all previous versions.
   * Each link typically includes:

     * **Parent Version ID**
     * **Signature** from the entity who created or validated that link.

3. **Signature Bundle**

   * Contains multiple signatures from potential keyholders (the user, a cryptographic authority, or an automated sign-off system).
   * Ensures multi-party trust in the shard’s origin and content.

4. **Metadata & Policy Flags**

   * May include policy information such as allowable read/write contexts in the Lattice, expiration timers, or special retention rules.

5. **Version ID**

   * Could be a human-readable `Major.Minor.Patch` or a deterministic hash-based scheme:

     * e.g., `v2.1.0` or `hash-based: 7ecf349b1…`.

---

## 4. Resilience & Security Considerations

1. **Replay Attacks**

   * The Edge uses ephemeral session tokens and timestamps to prevent an old shard upload from being replayed maliciously.
2. **Tamper Detection**

   * The Merkle-based chunk verification and final hash check quickly detect any tampered data in transit.
3. **Dual Registry**

   * The CCML Node maintains a local ledger of transfers, ensuring that if the Lattice fails or the network drops mid-transfer, the handshake can resume or revert gracefully.
4. **Version Conflicts**

   * If the user attempts to upload a new shard version without referencing the correct prior version, the Lattice can reject the commit, forcing the user to rebase or reconcile merges.

---

## 5. Example Handshake Sequence (Simplified)

1. **CCML → Confluence Edge**:

   ```
   Hello { 
       protocol_versions: [2.0, 2.1],
       shard_manifest: {...},
       ephemeral_key: ...
   }
   ```
2. **Confluence Edge → CCML**:

   ```
   Hello-Ack { 
       chosen_protocol: 2.1,
       session_token: "EDGE-SESSION-12345"
   }
   ```
3. **CCML → Confluence Edge** (Provenance):

   ```
   ShardHeader { 
       version_id: "v2.1.0",
       provenance_chain: [...],
       signatures: {...},
       auth_token: ...
   }
   ```
4. **Edge verifies** → If OK, requests payload chunks.
5. **CCML → Edge**: Streams encrypted shards in chunks (each chunk with partial hash).
6. **Edge** reconstructs → Commits to Lattice Registry →

   ```
   Commit-Ack {
       registry_id: "ONEIRIC-7ecf349b1",
       success: true
   }
   ```
7. **(Optional) Rollback**: If triggered,

   ```
   Rollback-Intent {
       version_id: "v2.1.0",
       reason: "Mismatch or user-initiated revert"
   }
   ```

   * Lattice reverts to the prior canonical version in the registry.

---

## 6. Conclusion

The **Oneiric Lattice Hand-Off Contract** formalizes a secure, verifiable, and easily reversible data transfer handshake between CCML and the Lattice environment. By combining **versioning**, **provenance proofs**, and **rollback hooks**, it ensures each shard transitions into the Oneiric Lattice with integrity and traceability. This design protects against tampering, clarifies lineage, and provides the necessary safety valves for graceful recovery from errors or user-initiated reverts.