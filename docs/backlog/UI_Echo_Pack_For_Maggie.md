# UI Echo Pack for Maggie – Author’s Preface Pressure‑Test

> Goal: translate the Sprint‑Zero loop into clickable, color‑coded mockups so we can usability‑test the 33‑shard flow.

---

## 1 · Core Screens

| Screen                     | Key Elements                                                                                        | Notes                                                                                   |
| -------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| **Shard Reader**           | 100‑word shard text block · Corpus symbol (SVG) top‑left · `Ask` textbox beneath · "Diffuse" button | Use the shard’s **symbol color** as border + accent; text on neutral background.        |
| **Recommendations Drawer** | Slide‑up panel listing top‑N enriched shards (title + nutrient bar)                                 | Each card shows miniature symbol + nutrient score bar (gradient same hue, 30% opacity). |
| **Vault Timeline**         | Horizontal scrollable ribbon at bottom; saved cards stack chronologically                           | Cards keep shard border color; hover shows note preview.                                |
| **Consent Modal**          | Checkbox matrix for text / embeddings / biosignals                                                  | Pull styling from existing MPC consent dialog.                                          |

## 2 · Color & Symbol Logic

* Adopt **CSL rotation spec**: 0° Read, 90° Ask, 180° Receive, 270° Index.
* Primary shard color = HEX pulled from `symbol_id` lookup.
* Nutrient bar uses same hue, 30‑70% opacity ramp.

## 3 · Interaction Echoes

1. **Diffuse Pulse** – on `Diffuse` click, symbol does 0°→90° spin then glows until response arrives.
2. **Vault Drop** – when user saves, shard card animates downward into ribbon; brief sparkle with symbol color.
3. **Priority Flash** – pro o1 weight ≥0.8 edges outlined thicker for 400 ms.

## 4 · Asset Checklist

* [ ] SVG set: 16 primary Corpus symbols (already supplied) + rotated variants.
* [ ] Color palette JSON mapping `symbol_id` → Tailwind class.
* [ ] Figma frame: *Shard Reader* (mobile + desktop).
* [ ] Figma component library: **Card**, **Drawer**, **RibbonItem**.

## 5 · Open Questions for Maggie

1. Do we keep recommendations in a drawer or inline below text?
2. Preference for scroll vs. drag in Vault ribbon?
3. Any motion guidelines we should respect beyond 200 ms/curve ease‑out?
4. Accessibility—contrast tweaks for dark mode?

### Deliverable Timeline

| Date       | Deliverable                                                    |
| ---------- | -------------------------------------------------------------- |
| **May 15** | Static Figma mockups for Shard Reader & Recommendations Drawer |
| **May 18** | Click‑through prototype including Vault ribbon animation       |
| **May 22** | Exported SVG/CSS asset pack to hand devs                       |

*Ping devs in Discord #ui-sync when first draft is ready.*
