# Six‑Week Agile Roadmap – *Author’s Preface Pressure‑Test ➜ MVP*  (2025‑05‑13 → 2025‑06‑24)

| **Week**            | **Sprint Theme**               | **Key Deliverables**                                                                                                                                                                            | **Owner(s)**           | **Exit Criteria**                                                |
| ------------------- | ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- | ---------------------------------------------------------------- |
| **0 (Sprint‑Zero)** | Setup & Loop Proof             | ✓ `loop-spec.md` implemented<br>✓ `GET /shards`, `POST /mnr/diffuse`, `POST /vault/save` live on localhost<br>✓ Latency <2 s E2E in dev                                                         | Backend (You), MNR dev | Lighthouse report shows p95 ≤2 s                                 |
| **1**               | **MNR Alpha**                  | ✓ Graph schema seeded with 33 shards<br>✓ Diffusion algorithm (k‑step) passing unit tests<br>✓ `pro o1` bus stub (Redis Streams) online                                                         | Backend, MNR           | CI green on MNR test suite; pro o1 publishes/consumes 100 msgs/s |
| **2**               | **UI Echo v1**                 | ✓ Figma mockups for Reader, Drawer, Vault<br>✓ React components scaffolded (Card, Drawer, RibbonItem)<br>✓ Color/symbol registry JSON merged                                                    | Maggie (UI)            | Click‑through demo on Vercel; meets WCAG AA                      |
| **3**               | **Vault & Consent**            | ✓ Vault Service w/ encryption at rest<br>✓ Consent Modal integrated (checkbox matrix)<br>✓ GDPR delete flow prototype (`DELETE /vault/:entry_id`)                                               | Backend, Policy        | Data scrub executes within 150 ms; consent events logged         |
| **4**               | **Protein‑Fold & pro o1 Beta** | ✓ `protein-fold.md` runtime operational (symbol rotations trigger state changes)<br>✓ Message envelope & TypeScript interface deployed<br>✓ Priority weighting live, visible in Redux dev‑tools | Backend, Frontend      | Fold action updates UI state and logs via pro o1                 |
| **5**               | **Cross‑Device QA**            | ✓ Mobile layout polish (tailwind breakpoints)<br>✓ Manual test matrix across Chrome/Safari/Firefox + iOS/Android<br>✓ Latency audit & cache tuning                                              | Maggie, QA             | p95 <2 s on mobile 4G; no critical bugs                          |
| **6**               | **Soft Launch (MVP‑Alpha)**    | ✓ User onboarding (magic‑link login)<br>✓ 10 pilot users run through Read→Ask→Receive→Save flow<br>✓ Feedback captured in GitHub Issues                                                         | Team                   | 80% users complete loop without guidance, NPS > +30              |

---

## Stretch Goals (if capacity remains)

1. **MNR Visualization** – real‑time graph explorer in dev tools.
2. **Biosignal Hook (NFSL)** – heart‑rate dummy data influencing nutrient scores.
3. **Magical Bonds v0** – link two users so their Vault saves cross‑pollinate.

---

*Next revision due after Week 2 retro.*