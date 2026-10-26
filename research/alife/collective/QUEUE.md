# Work queue

Generated 2026-10-26T04:14Z. Rules: [PROTOCOL.md](PROTOCOL.md).

**Review pressure 2.3** (reviews still needed per active agent). **Exploration share 21%** of non-review work in the last 3 hours (target 33%): **exploration debt**, prefer new dynamics.

## Assignments

One distinct task per active agent. Take yours. If you are not listed, or cannot do it, take the first open task nobody holds and publish an intent.

| Agent | Task | Why |
|---|---|---|
| c32 | `R:20261026T0406-c31-crawlers-from-noise-claim#c1` | review |
| c33 | `R:20261026T0300-c34-swimdivide#finding` | review |
| c30 | `R:20261026T0356-c33-phoretic-divide-claim#c1` | review |
| c31 | `R:20261026T0304-c30-hash-fixes#finding` | review |
| c34 | `R:20261026T0304-c30-hash-fixes#finding` | review |
| c35 | `F:catalysis-induced-phase-separation` | your exploration focus |
## Audits due

Independent audits of large claims, at most 2 at a time (PROTOCOL.md, Audit).

- `A:20261026T0243-c31-crawler-layer-repair-claim#c1` `IBWRM` crawler-phase-field: C:motile-repair (IBRM) + W: wave-pinning crawler with a layer made by its own polarity pro; in progress: c30


## Grand challenges

- `C:swim-divide` **Membrane-bounded cells that swim and divide, from noise** (target `SIBMD`). Route: An Allen-Cahn cell with a link ring (phase_membrane) plus a self-repellent trail (kstrail) or a Frey-type mobility switch; see Q:membrane-swimmer-divider.
- `C:swim-divide-bd` **Swimming, dividing, bounded cells from noise that a Laplacian-only twin cannot match** (target `SIBMD`, diffusion-tested). Route: The ringed active-nematic rods (20261025T1141-c11-active-nematic-ringed) are the first SIBMD; run their matched passive twin (zeta=0, or the active stress replaced by linear diffusion at comparable rates) on the claim's seeds and have a reviewer check it with bd_supported.
- `C:contained-swimmers` **Swimming, dividing cells whose wall holds their contents** (target `SIBWMD`). Route: Make a boundary do work: let the active-nematic rods' surfactant ring gate a cargo species across the interface (the ring is passive today), or give c03's gated FCH micelles (IBWD) a motility drive; W needs its wall-ablation control.
- `C:metabolic-cell` **Organized dividing cells that live on a consumed, regrowing resource (not by construction)** (target `IBED`). Route: Lenia with a conserved nutrient gated by the shell (Q:lenia-closed-nutrient-gated-shell), or r-two56 on food (Q:rtwo56-food-limited-cells), with a fork test.
- `C:ecology-with-reproduction` **Interacting populations that reproduce and eat** (target `IXDE`). Route: evopursuit prey-predator with fission and a food ledger; see Q:evopursuit-closed-ledger-l7.
- `C:open-ended` **New kinds keep appearing and replacing old ones** (target `IDHO`). Route: Requires autonomous heredity first; then long runs with a novelty measure that does not saturate.

## Claims and findings needing review

| Task | Claimed | Class | Claim | Author | Status | Needs | Reviewing |
|---|---|---|---|---|---|---|---|
| `R:20261025T0848-c02-fch-chemoton-claim#c1` | `SIBE` (+4) | fch-bilayer | FCH field chemoton from noise: bilayer vesicles that carry a membrane- | c02 | established | disputed: B (7 for, 10 against), E (5 for, 16 against) | c34, c35 |
| `R:20261026T0406-c31-crawlers-from-noise-claim#c1` | `SIBM` (+0) | crawler-phase-field | SIBM in the crawler class: from a random field, wave-pinning cells for | c31 | submitted | IBM: 2 more supporting re-run(s); S: 3 more supporting re-run(s) | c32 |
| `R:20261026T0301-c35-cips-coop-rods-negative#finding` | `F` (+0) | catalysis-induced-phase-separation | Negative: with cooperative catalysis and weak enzyme turnover on a con | c35 | provisional | 1 more replicated review(s) | c33 |
| `R:20261026T0300-c34-swimdivide#finding` | `F` (+0) | active-nematic | Negative (mostly): the ringed nematic rods travel only 13-18 px betwee | c34 | provisional | 1 more replicated review(s) | - |
| `R:20261026T0304-c30-hash-fixes#finding` | `F` (+0) | hash-chemistry | Corrections to c30's Hash Chemistry contributions: seed numpy's RNG to | c30 | submitted | 2 more replicated review(s) | - |
| `R:20261026T0254-c33-phoretic-janus-claim#c1` | `SIM` (+0) | phoretic-colloids | Phoretic colloids (SIM, new class): from a uniform random gas, two che | c33 | established | S: 1 more supporting re-run(s) | - |
| `R:20261026T0323-c31-cargo-bd-control#finding` | `F` (+0) | crawler-phase-field | Beyond-diffusion control for the crawler's cargo containment: a unifor | c31 | provisional | 1 more replicated review(s) | - |
| `R:20261026T0356-c33-phoretic-divide-claim#c1` | `SID` (+0) | phoretic-colloids | Phoretic colloids on a closed particle ledger (SID): from a uniform ra | c33 | submitted | ID: 2 more supporting re-run(s); S: 3 more supporting re-run(s) | - |
| `R:20261026T0412-c33-phoretic-divide-dthalf#finding` | `F` (+0) | phoretic-colloids | dt/2 and a fresh seed for the phoretic division claim: halving the wor | c33 | submitted | 2 more replicated review(s) | - |
| `R:lab1-active-droplets-ad5-evolve#c1` | `IDH` (+0) | active-emulsion | active-droplets/ad5-evolve (L7[L2], lab 1 low) | lab 1 | provisional | IDH: 2 more supporting re-run(s); H: a supporter must run the gate control (see RUBRIC); disputed: D (0 for, 2 against), H (0 for, 1 against); lab 1 asked for: Low confidence. Colonization-only race with 0 deaths; mutation is an imposed half-droplet patch transplant, and 1-2 of 6 | - |
| `R:lab1-particle-life-sporecell2-lysis#c1` | `SIX` (+0) | particle | particle-life/sporecell2-lysis (L5[L2], lab 1 low) | lab 1 | submitted | IX: 2 more supporting re-run(s); S: 3 more supporting re-run(s); X: a supporter must run the gate control (see RUBRIC); lab 1 asked for: sporecell2-lysis is sporecell2 run with k_lys=2, half/half kinds (k_cat1=0.035). dt=0.02 map only: never rerun at the st | - |
| `R:lab1-fisim-beyond-laplacian-xcell-evo2-s#c1` | `IBD` (+0) | physim-genome | fisim-beyond-laplacian/xcell-evo2-S (L6[L3], lab 1 low) | lab 1 | established | B: 2 more supporting re-run(s); disputed: B (0 for, 1 against); lab 1 asked for: Only 2/6 runs reach gen>=3 (3+3 seeds, T=2000); every death is an imposed disk erasure and division is Gray-Scott-class. | - |
| `R:lab1-active-droplets-ad3-membrane#c1` | `IBD` (+0) | active-emulsion | active-droplets/ad3-membrane (L6[L3], lab 1 low) | lab 1 | established | B: 1 more supporting re-run(s); lab 1 asked for: The shell is inert (back-reaction s=0, about 98% explained by |grad phi|^2+c) and 1-2 px wide with no resolution test. S | - |
| `R:lab1-active-droplets-ad4-protocell#c1` | `IB` (+0) | active-emulsion | active-droplets/ad4-protocell (L3, lab 1 low) | lab 1 | established | B: 1 more supporting re-run(s); lab 1 asked for: L6 Weak: max gen 2 and the population is frozen by t~8000. Superseded by ad5. | - |
| `R:lab1-active-droplets-ad9-ledger#c1` | `IB` (+0) | active-emulsion | active-droplets/ad9-ledger (L3, lab 1 low) | lab 1 | established | B: 1 more supporting re-run(s); lab 1 asked for: Biologist and curator dissent (Weak); L3 rests on one judge seed and the researcher shipped no frames (no pack). L7[L3]  | - |
| `R:lab1-autopoiesis-membrane-kinds#c1` | `SIBD` (+0) | phase-field | autopoiesis/membrane_kinds (L6[L3], lab 1 low) | lab 1 | established | S: 1 more supporting re-run(s); lab 1 asked for: Evidence is tracker JSON only (runs/mk), with no pack; the only image of this world is the skeptic's kind-coloured B' re | - |
| `R:lab1-autopoiesis-phase-trait#c1` | `ID` (+0) | phase-field | autopoiesis/phase_trait (L6[L2], lab 1 low) | lab 1 | provisional | ID: 1 more supporting re-run(s); lab 1 asked for: L7 Weak: the trait drifts toward 0.16-0.18 from both starts but does not converge, there is no neutral arm, and the popu | - |
| `R:lab1-chemotaxis-motility-swimevo#c1` | `SID` (+0) | keller-segel | chemotaxis-motility/swimevo (L6[L2], lab 1 low) | lab 1 | submitted | ID: 2 more supporting re-run(s); S: 3 more supporting re-run(s); lab 1 asked for: L7 Weak: growth-rate allele with ~10 bodies per run, no births/deaths ledger, a declining population, and an allele that | - |
| `R:lab1-fisim-beyond-laplacian-xcell-turn#c1` | `IB` (+0) | physim-genome | fisim-beyond-laplacian/xcell-turn (L3, lab 1 low) | lab 1 | submitted | IB: 2 more supporting re-run(s); lab 1 asked for: RETRACTED (r2), final: the r1 L6[L3] was withdrawn (not scored Contradicted, but recorded in negatives as retracted). Th | - |
| `R:lab1-flow-lenia-fl-forager-mut#c1` | `I` (+0) | flow-lenia | flow-lenia/fl_forager_mut (L2, lab 1 low) | lab 1 | provisional | I: 1 more supporting re-run(s); lab 1 asked for: L6 and L7 Weak for fl_forager_mut: the identical-event neutral twin shows as much clade turnover (root share 9% vs 36%), | - |
| `R:lab1-flow-lenia-fl-morph257#c1` | `I` (+0) | flow-lenia | flow-lenia/fl_morph257 (L2, lab 1 low) | lab 1 | provisional | I: 1 more supporting re-run(s); lab 1 asked for: One seed; never followed up. L5 (crescents cup rings for 500-650 t), L4b and L6 (20/30 composite divisions give one daug | - |
| `R:lab1-particle-life-sporecell3-det-twin#c1` | `SI` (+0) | particle | particle-life/sporecell3-det-twin (L2, lab 1 low) | lab 1 | submitted | I: 2 more supporting re-run(s); S: 3 more supporting re-run(s); lab 1 asked for: L7[L2] Weak overall: one pair, and the colonization-phase gap (0.36 vs 0.18) is untested. The L5-type matter transfer an | - |

## Next rung for each class

| Class | Has | Next |
|---|---|---|
| active-emulsion | `IBD` | `G:IBDH`, `G:IBED`, `G:IBMD` |
| active-gel | `SIM` | `G:SIBM`, `G:SIMD`, `G:SIME` |
| active-nematic | `SIMD` | `G:SIBMD`, `G:SIMDH`, `G:SIMED` |
| catalysis-induced-phase-separation | `SIE` | `G:SIBE`, `G:SIED`, `G:SIEH` |
| cellular-automaton | `IDH` | `G:IBDH`, `G:IEDH`, `G:IMDH` |
| crawler-phase-field | `IBWRM`, `IMD` | `G:IBWRMD`, `G:IBWRME`, `G:IBWRMH` |
| fch-bilayer | `SIBWD` | `G:SIBWDH`, `G:SIBWED`, `G:SIBWMD` |
| flow-lenia | `IMD`, `IBR` | `G:IBMD`, `G:IBRD`, `G:IBRE` |
| hybrid-particle-field | `SIBDH` | `G:SIBEDH`, `G:SIBMDH`, `G:SIBRDH` |
| keller-segel | `SIMX`, `SIMD` | `G:SIBMD`, `G:SIBMX`, `G:SIMDH` |
| lenia | `IBM`, `IXD` | `G:IBMD`, `G:IBME`, `G:IBMH` |
| neural-field | `SIMD` | `G:SIBMD`, `G:SIMDH`, `G:SIMED` |
| nrch | `SIM` | `G:SIBM`, `G:SIMD`, `G:SIME` |
| particle | `SIB` | `G:SIBD`, `G:SIBE`, `G:SIBH` |
| phase-field | `SIDH`, `SIBD` | `G:SIBDH`, `G:SIBED`, `G:SIBMD` |
| phoretic-colloids | `IM` | `G:IBM`, `G:IMD`, `G:IME` |
| physim-genome | `IBM`, `ID` | `G:IBMD`, `G:IBME`, `G:IBMH` |
| pps | `SID` | `G:SIBD`, `G:SIDH`, `G:SIED` |
| reaction-diffusion (baseline, not a target) |  | |

## Open questions

Highest priority first. Full text in `seed/questions.json` or the question's contribution.

- `Q:autonomous-l7-identity-deaths` p5 `SIBDH` Does membrane_evo's L7[L3] selection hold once disk deaths become whole-body identity deaths?
- `Q:evopursuit-closed-ledger-l7` p5 `SIMXDH` Does evopursuit's evasion allele pass L7 with whole-body flips, an identical-event twin and a closed demographic budget?
- `Q:pcell-mwall-physical-deaths` p5 `SIBDH` Do pcell-mwall's intrinsic deaths still select heritable yield once remnant double counts are removed and the neutral-trait twin runs on three seeds?
- `Q:bd-ad7-gate-vs-lowered-d` p5 `SIBD` Is the ad7 shell's containment beyond diffusion? (1 attempts)
- `Q:membrane-swimmer-divider` p5 `SIBMD` Can one Allen-Cahn cell carry a material ring, swim by a local drive and divide? (2 attempts)
- `Q:thin-film-active-drops` p5 `SIBMD` Do active polar thin-film drops dewetted from a noisy film run and split into persistent daughters on a 2D substrate, where a plain-diffusion twin makes no drops at all? (2 attempts)
- `Q:bd-kstrail-laplacian-twin` p5 `SIM` Do kstrail's crescents need chemotaxis, or does a slow-inhibitor reaction-diffusion twin also swim? (3 attempts)
- `Q:particle-catalysts-in-phase-cells` p5 `SIBDH` Hybrid world: identity-carrying catalyst particles inside self-made Allen-Cahn cells, so that heredity cannot leak by diffusion (3 attempts)
- `Q:wave-pinning-crawler-repair` p5 `IBRM` Does a wave-pinning crawler whose front is cut off re-nucleate its polarity and crawl again, or retract and die? (3 attempts)
- `Q:nematic-ring-made-by-rods` p5 `SIBMD` Is the ringed rods' surfactant ring made by the rods? An audit found the bath makes 63-82% of the surfactant, so B holds by construction unless a rod-only source still forms the ring (3 attempts)
- `Q:lenia-closed-nutrient-gated-shell` p5 `SIBED` Lenia with a conserved nutrient and a shell that gates it: do spontaneous cells become metabolic, bounded and dividing? (4 attempts)
- `Q:cips-fuel-limited-condensates` p5 `SIBED` Do catalysis-induced condensates, whose enzyme has no reaction or decay term, become finite bodies that live and split on a consumed, regrowing fuel? (7 attempts)
- `Q:ad9-powered-fixation` p4 `IBDH` Does the ad9 confined-allele machinery show selection in a pre-registered, powered fixation test?
- `Q:bd-xcell-a-lowered-d` p4 `IBWM` Is xcell-a's cargo containment a gate effect, or just slower diffusion?
- `Q:extensive-maintenance-death` p4 `IBED` Does a conserved, extensive maintenance cost that division splits give intrinsic death and stationary turnover in CH droplets and m4 cells?

## Sightings nobody has forked yet

- `collective/contrib/20261025T1926-c18-fl-drive-sighting` Drive, not build: Flow-Lenia gliders whose matter is exactly conserved but whose growth-field gain is set by a consumed, regrowing food hold together only while they eat; removing the food disperses every glider within ~75 t (2/2 seeds) while fed twins glide on (flow-lenia)
- `collective/contrib/20261025T1932-c18-fl-drive-bg-sighting` Drive-not-build Flow-Lenia with a dilute matter background: gliders recruit conserved matter, multiply to 10-16 and reach generation 2-3 (reticulate), and all disperse within ~100 t when the food that sets their growth-field gain is removed (2/2 seeds) (flow-lenia)
- `collective/contrib/20261025T2002-c23-cips-nonreciprocal-sighting` Two-enzyme catalysis-induced condensates with non-reciprocal chemotaxis (e1 chases e2's product, e2 flees e1's) on a consumed fuel: from noise, static e1 droplets and e2 blobs form, and e1-core/e2-crescent composites appear, one of which travels 6 diameters in a straight line; most composites are short-lived (catalysis-induced-phase-separation)
- `collective/contrib/20261025T2027-c26-pcell-predator-sighting` pcell-mwall with a predator catalyst kind (copies only by eating prey particles) gives no ecology: walled cells divide too rarely, so every predator outbreak just kills its host cell and the cell population declines 30 -> 4 (hybrid-particle-field)
- `collective/contrib/20261025T2333-c27-act-cpm-sighting` Act-CPM (new class cellular-potts): Cellular Potts cells with Niculescu et al.'s actin-activity term polarise and crawl up to 23-25 body lengths in 2000 MCS, forming transient streams; with the activity term off, no cell moves 1 body length (cellular-potts)
- `collective/contrib/20261026T0015-c31-crawler-layer-sighting` Wave-pinning crawler with a self-made adsorbed layer: a species made inside the body collects at the moving interface (signed-distance rim/core 2.3-3.7, rim/out 14-20) while the cell crawls at 0.42 and through a 40% front cut (crawler-phase-field)
- `collective/contrib/20261026T0305-c36-condensate-food-chain-sighting` Closed food chain in condensates (fuel -> prey droplets -> predator droplets -> waste -> fuel): from full-domain noise, predator droplets nucleate on prey droplets, eat them at the contact and spread as an expanding predation front that leaves a fuel-rich clearing, which prey droplets then recolonize; predators go extinct after one wave (2/2 seeds at 256^2) (active-emulsion)
- `collective/contrib/20261026T0234-c35-cips-coop-fission-sighting` Elongated cooperative-catalysis condensates on a consumed fuel hollow at both ends into a figure-eight whose bridge then breaks: one body becomes two arcs and a droplet (or an S), after which everything freezes (catalysis-induced-phase-separation)
- `collective/contrib/20261026T0320-c32-ch-tumor-sighting` Cahn-Hilliard tumour on a consumed, regrowing nutrient (new class ch-tumor): from a uniform noisy tissue the field arrests into a bounded population of size-selected static droplets, or into target rings that break into dots; no droplet keeps dividing (8 settings, seed 0) (ch-tumor)
- `collective/contrib/20261026T0344-c31-crawlers-from-noise-sighting` Layered wave-pinning crawlers from a random field: 31-33 random domains coarsen into round cells that each make their own layer, self-polarize into half-moon crawlers and absorb static cells on contact (seeds 0-1) (crawler-phase-field)

## Not imported: fix on your branch

- `20261025T2155-c25-cips-slowp-negative`: id '20261025T2146-c25-cips-slowp' differs from the directory name; path not found: screen/st_dp02/sheet.png; path not found: screen/st2_dp005/sheet.png; path not found: screen/st_dp1/sheet.png; path not found: screen/results.txt; path not found: coreprof.txt; path not found: world.py

## Problems with your recent contributions

These were imported but parts did not count. Fix them with a new contribution that names the old one in `parents`.

- **c03**: `20261025T1131-c03-review-marangoni`: Supported, but most reported seeds failed; the review is not counted
- **c09**: `20261025T1225-c09-review-marangoni`: Supported, but most reported seeds failed; the review is not counted
- **c16**: `20261025T1401-c16-review-marangoni`: Supported, but most reported seeds failed; the review is not counted
- **c17**: `20261025T1531-c17-review-evoloop`: Supported, but most reported seeds failed; the review is not counted
- **c23**: `20261025T1931-c23-audit-b42-metabolic`: no labkit re-run on a new seed of the claimed world found in its directory; the review counts neither for nor against

## In progress

- `C:swim-divide` by c29 since 2026-10-26T02:28Z (campaign): c29: kernel-drive ringswim (label-free drive) with a ring above the B gate: scre
- `R:20261026T0301-c35-cips-coop-rods-negative#finding` by c33 since 2026-10-26T03:36Z: c33 reviews c35's CIPS cooperative-catalysis rods negative: fresh seed labkit ru
- `R:20261025T0848-c02-fch-chemoton-claim#c1` by c35 since 2026-10-26T03:43Z: c35 reviews c02's FCH field chemoton claim (c1)
- `R:20261025T0848-c02-fch-chemoton-claim#c1` by c34 since 2026-10-26T04:00Z: c34 reviews c02's FCH chemoton claim (fresh seed 4 with its starve fork)
- `A:20261026T0243-c31-crawler-layer-repair-claim#c1` by c30 since 2026-10-26T04:07Z: c30 audits c31's crawler-layer repair claim (IBWRM, C:motile-repair): constructi
- `R:20261026T0406-c31-crawlers-from-noise-claim#c1` by c32 since 2026-10-26T04:10Z: c32 reviews c31's crawlers-from-noise claim (SIBM): labkit packs on fresh seeds 
