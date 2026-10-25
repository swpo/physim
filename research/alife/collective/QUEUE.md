# Work queue

Generated 2026-10-25T21:43Z. Rules: [PROTOCOL.md](PROTOCOL.md).

**Review pressure 0.6** (reviews still needed per active agent). **Exploration share 52%** of non-review work in the last 3 hours (target 33%).

## Assignments

One distinct task per active agent. Take yours. If you are not listed, or cannot do it, take the first open task nobody holds and publish an intent.

| Agent | Task | Why |
|---|---|---|
| c21 | `R:20261025T2101-c27-fch-gate-vs-slowdk#finding` | review |
| c23 | `R:20261025T2150-c22-wavepin-renucleation-claim#c1` | review |
| c24 | `R:20261025T2130-c23-cips-inhibitor-arrest#finding` | review |
| c25 | `R:20261025T1256-c16-evoloop-claim#c1` | your campaign |
| c27 | `R:20261025T2150-c22-wavepin-renucleation-claim#c1` | review |
| c28 | `C:swim-divide` | your campaign |
| c22 | `F:crawler-phase-field` | your exploration focus |
| c26 | `F:ecology` | your exploration focus |

## Grand challenges

- `C:swim-divide` **Membrane-bounded cells that swim and divide, from noise** (target `SIBMD`). Route: An Allen-Cahn cell with a link ring (phase_membrane) plus a self-repellent trail (kstrail) or a Frey-type mobility switch; see Q:membrane-swimmer-divider.
- `C:swim-divide-bd` **Swimming, dividing, bounded cells from noise that a Laplacian-only twin cannot match** (target `SIBMD`, diffusion-tested). Route: The ringed active-nematic rods (20261025T1141-c11-active-nematic-ringed) are the first SIBMD; run their matched passive twin (zeta=0, or the active stress replaced by linear diffusion at comparable rates) on the claim's seeds and have a reviewer check it with bd_supported.
- `C:contained-swimmers` **Swimming, dividing cells whose wall holds their contents** (target `SIBWMD`). Route: Make a boundary do work: let the active-nematic rods' surfactant ring gate a cargo species across the interface (the ring is passive today), or give c03's gated FCH micelles (IBWD) a motility drive; W needs its wall-ablation control.
- `C:metabolic-cell` **Organized dividing cells that live on a consumed, regrowing resource (not by construction)** (target `IBED`). Route: Lenia with a conserved nutrient gated by the shell (Q:lenia-closed-nutrient-gated-shell), or r-two56 on food (Q:rtwo56-food-limited-cells), with a fork test.
- `C:motile-repair` **Self-propelled organized individuals that repair** (target `IBRM`). Route: Damage a mature swimming cell (kstrail crescent with a wall, or an Allen-Cahn swimmer) with an undamaged twin.
- `C:ecology-with-reproduction` **Interacting populations that reproduce and eat** (target `IXDE`). Route: evopursuit prey-predator with fission and a food ledger; see Q:evopursuit-closed-ledger-l7.
- `C:open-ended` **New kinds keep appearing and replacing old ones** (target `IDHO`). Route: Requires autonomous heredity first; then long runs with a novelty measure that does not saturate.

## Claims and findings needing review

| Task | Claimed | Class | Claim | Author | Status | Needs | Reviewing |
|---|---|---|---|---|---|---|---|
| `R:20261025T0848-c02-fch-chemoton-claim#c1` | `SIBE` (+4) | fch-bilayer | FCH field chemoton from noise: bilayer vesicles that carry a membrane- | c02 | established | disputed: B (7 for, 7 against), E (5 for, 10 against) | - |
| `R:20261025T1256-c16-evoloop-claim#c1` | `IBDH` (+0) | cellular-automaton | Evoloop: sheathed self-replicating CA loops whose size mutates in coll | c16 | established | disputed: H (5 for, 5 against) | c25 |
| `R:20261025T2022-c21-b42-deaths-are-founders#finding` | `F` (+0) | hybrid-particle-field | Addendum to my pcell-mwall-b42 audit: 78 of 82 mature deaths (>= 10000 | c21 | provisional | 1 more replicated review(s) | c24 |
| `R:20261025T2101-c27-fch-gate-vs-slowdk#finding` | `F` (+0) | fch-bilayer | The FCH chemoton's bilayer gate does what no uniform catalyst diffusiv | c27 | provisional | 1 more replicated review(s) | - |
| `R:20261025T2104-c22-wavepin-repair-numerics#finding` | `F` (+0) | crawler-phase-field | The wave-pinning crawler's front-cut repair survives 1.5x resolution ( | c22 | provisional | 1 more replicated review(s) | c27 |
| `R:20261025T2130-c23-cips-inhibitor-arrest#finding` | `F` (+0) | catalysis-induced-phase-separation | A catalysis inhibitor made by catalysis arrests the coarsening of cata | c23 | provisional | 1 more replicated review(s) | - |
| `R:20261025T2134-c26-ecopursuit-fission-fusion#finding` | `F` (+0) | keller-segel | Negative for C:ecology-with-reproduction via evopursuit: predators rai | c26 | submitted | 2 more replicated review(s) | c22, c23 |
| `R:20261025T2150-c22-wavepin-renucleation-claim#c1` | `IRM` (+0) | crawler-phase-field | Front re-nucleation in the wave-pinning crawler: after a 40% front cut | c22 | submitted | IRM: 2 more supporting re-run(s); R: a supporter must run the gate control (see RUBRIC) | - |
| `R:lab1-active-droplets-ad5-evolve#c1` | `IDH` (+0) | active-emulsion | active-droplets/ad5-evolve (L7[L2], lab 1 low) | lab 1 | provisional | IDH: 2 more supporting re-run(s); H: a supporter must run the gate control (see RUBRIC); disputed: D (0 for, 1 against); lab 1 asked for: Low confidence. Colonization-only race with 0 deaths; mutation is an imposed half-droplet patch transplant, and 1-2 of 6 | - |
| `R:lab1-fisim-beyond-laplacian-xcell-evo2-s#c1` | `IBD` (+0) | physim-genome | fisim-beyond-laplacian/xcell-evo2-S (L6[L3], lab 1 low) | lab 1 | submitted | IBD: 2 more supporting re-run(s); lab 1 asked for: Only 2/6 runs reach gen>=3 (3+3 seeds, T=2000); every death is an imposed disk erasure and division is Gray-Scott-class. | - |
| `R:lab1-particle-life-sporecell2-lysis#c1` | `SIX` (+0) | particle | particle-life/sporecell2-lysis (L5[L2], lab 1 low) | lab 1 | submitted | IX: 2 more supporting re-run(s); S: 3 more supporting re-run(s); X: a supporter must run the gate control (see RUBRIC); lab 1 asked for: sporecell2-lysis is sporecell2 run with k_lys=2, half/half kinds (k_cat1=0.035). dt=0.02 map only: never rerun at the st | - |
| `R:lab1-active-droplets-ad3-membrane#c1` | `IBD` (+0) | active-emulsion | active-droplets/ad3-membrane (L6[L3], lab 1 low) | lab 1 | submitted | IBD: 2 more supporting re-run(s); lab 1 asked for: The shell is inert (back-reaction s=0, about 98% explained by |grad phi|^2+c) and 1-2 px wide with no resolution test. S | - |
| `R:lab1-active-droplets-ad4-protocell#c1` | `IB` (+0) | active-emulsion | active-droplets/ad4-protocell (L3, lab 1 low) | lab 1 | submitted | IB: 2 more supporting re-run(s); lab 1 asked for: L6 Weak: max gen 2 and the population is frozen by t~8000. Superseded by ad5. | - |
| `R:lab1-active-droplets-ad9-ledger#c1` | `IB` (+0) | active-emulsion | active-droplets/ad9-ledger (L3, lab 1 low) | lab 1 | submitted | IB: 2 more supporting re-run(s); lab 1 asked for: Biologist and curator dissent (Weak); L3 rests on one judge seed and the researcher shipped no frames (no pack). L7[L3]  | - |
| `R:lab1-autopoiesis-membrane-kinds#c1` | `SIBD` (+0) | phase-field | autopoiesis/membrane_kinds (L6[L3], lab 1 low) | lab 1 | submitted | IBD: 2 more supporting re-run(s); S: 3 more supporting re-run(s); lab 1 asked for: Evidence is tracker JSON only (runs/mk), with no pack; the only image of this world is the skeptic's kind-coloured B' re | - |
| `R:lab1-autopoiesis-phase-trait#c1` | `ID` (+0) | phase-field | autopoiesis/phase_trait (L6[L2], lab 1 low) | lab 1 | submitted | ID: 2 more supporting re-run(s); lab 1 asked for: L7 Weak: the trait drifts toward 0.16-0.18 from both starts but does not converge, there is no neutral arm, and the popu | - |
| `R:lab1-chemotaxis-motility-swimevo#c1` | `SID` (+0) | keller-segel | chemotaxis-motility/swimevo (L6[L2], lab 1 low) | lab 1 | submitted | ID: 2 more supporting re-run(s); S: 3 more supporting re-run(s); lab 1 asked for: L7 Weak: growth-rate allele with ~10 bodies per run, no births/deaths ledger, a declining population, and an allele that | - |
| `R:lab1-fisim-beyond-laplacian-xcell-turn#c1` | `IB` (+0) | physim-genome | fisim-beyond-laplacian/xcell-turn (L3, lab 1 low) | lab 1 | submitted | IB: 2 more supporting re-run(s); lab 1 asked for: RETRACTED (r2), final: the r1 L6[L3] was withdrawn (not scored Contradicted, but recorded in negatives as retracted). Th | - |
| `R:lab1-flow-lenia-fl-forager-mut#c1` | `I` (+0) | flow-lenia | flow-lenia/fl_forager_mut (L2, lab 1 low) | lab 1 | submitted | I: 2 more supporting re-run(s); lab 1 asked for: L6 and L7 Weak for fl_forager_mut: the identical-event neutral twin shows as much clade turnover (root share 9% vs 36%), | - |
| `R:lab1-flow-lenia-fl-morph257#c1` | `I` (+0) | flow-lenia | flow-lenia/fl_morph257 (L2, lab 1 low) | lab 1 | submitted | I: 2 more supporting re-run(s); lab 1 asked for: One seed; never followed up. L5 (crescents cup rings for 500-650 t), L4b and L6 (20/30 composite divisions give one daug | - |
| `R:lab1-particle-life-sporecell3-det-twin#c1` | `SI` (+0) | particle | particle-life/sporecell3-det-twin (L2, lab 1 low) | lab 1 | submitted | I: 2 more supporting re-run(s); S: 3 more supporting re-run(s); lab 1 asked for: L7[L2] Weak overall: one pair, and the colonization-phase gap (0.36 vs 0.18) is untested. The L5-type matter transfer an | - |

## Next rung for each class

| Class | Has | Next |
|---|---|---|
| active-emulsion | `IBD` | `G:IBDH`, `G:IBED`, `G:IBMD` |
| active-gel | `SIM` | `G:SIBM`, `G:SIMD`, `G:SIME` |
| active-nematic | `SIMD` | `G:SIBMD`, `G:SIMDH`, `G:SIMED` |
| catalysis-induced-phase-separation | `SIE` | `G:SIBE`, `G:SIED`, `G:SIEH` |
| cellular-automaton | `ID` | `G:IBD`, `G:IDH`, `G:IED` |
| crawler-phase-field | `IMD`, `IRM` | `G:IBMD`, `G:IBRM`, `G:IMDH` |
| fch-bilayer | `SIBWD` | `G:SIBWDH`, `G:SIBWED`, `G:SIBWMD` |
| flow-lenia | `IMD`, `IBR` | `G:IBMD`, `G:IBRD`, `G:IBRE` |
| hybrid-particle-field | `SIBDH` | `G:SIBEDH`, `G:SIBMDH`, `G:SIBRDH` |
| keller-segel | `SIMX`, `SIMD` | `G:SIBMD`, `G:SIBMX`, `G:SIMDH` |
| lenia | `IBM`, `IXD` | `G:IBMD`, `G:IBME`, `G:IBMH` |
| neural-field | `SIMD` | `G:SIBMD`, `G:SIMDH`, `G:SIMED` |
| nrch | `SIM` | `G:SIBM`, `G:SIMD`, `G:SIME` |
| particle | `SIB` | `G:SIBD`, `G:SIBE`, `G:SIBH` |
| phase-field | `SIDH`, `SIBD` | `G:SIBDH`, `G:SIBED`, `G:SIBMD` |
| physim-genome | `IBM` | `G:IBMD`, `G:IBME`, `G:IBMH` |
| reaction-diffusion (baseline, not a target) |  | |

## Open questions

Highest priority first. Full text in `seed/questions.json` or the question's contribution.

- `Q:autonomous-l7-identity-deaths` p5 `SIBDH` Does membrane_evo's L7[L3] selection hold once disk deaths become whole-body identity deaths?
- `Q:evopursuit-closed-ledger-l7` p5 `SIMXDH` Does evopursuit's evasion allele pass L7 with whole-body flips, an identical-event twin and a closed demographic budget?
- `Q:pcell-mwall-physical-deaths` p5 `SIBDH` Do pcell-mwall's intrinsic deaths still select heritable yield once remnant double counts are removed and the neutral-trait twin runs on three seeds?
- `Q:nematic-ring-made-by-rods` p5 `SIBMD` Is the ringed rods' surfactant ring made by the rods? An audit found the bath makes 63-82% of the surfactant, so B holds by construction unless a rod-only source still forms the ring; in progress: c21
- `Q:bd-ad7-gate-vs-lowered-d` p5 `SIBD` Is the ad7 shell's containment beyond diffusion? (1 attempts)
- `Q:membrane-swimmer-divider` p5 `SIBMD` Can one Allen-Cahn cell carry a material ring, swim by a local drive and divide? (2 attempts)
- `Q:thin-film-active-drops` p5 `SIBMD` Do active polar thin-film drops dewetted from a noisy film run and split into persistent daughters on a 2D substrate, where a plain-diffusion twin makes no drops at all? (2 attempts)
- `Q:bd-kstrail-laplacian-twin` p5 `SIM` Do kstrail's crescents need chemotaxis, or does a slow-inhibitor reaction-diffusion twin also swim? (3 attempts)
- `Q:particle-catalysts-in-phase-cells` p5 `SIBDH` Hybrid world: identity-carrying catalyst particles inside self-made Allen-Cahn cells, so that heredity cannot leak by diffusion (3 attempts)
- `Q:cips-fuel-limited-condensates` p5 `SIBED` Do catalysis-induced condensates, whose enzyme has no reaction or decay term, become finite bodies that live and split on a consumed, regrowing fuel? (3 attempts)
- `Q:wave-pinning-crawler-repair` p5 `IBRM` Does a wave-pinning crawler whose front is cut off re-nucleate its polarity and crawl again, or retract and die? (3 attempts)
- `Q:lenia-closed-nutrient-gated-shell` p5 `SIBED` Lenia with a conserved nutrient and a shell that gates it: do spontaneous cells become metabolic, bounded and dividing? (4 attempts)
- `Q:ad9-powered-fixation` p4 `IBDH` Does the ad9 confined-allele machinery show selection in a pre-registered, powered fixation test?
- `Q:bd-rtwo56-dog-twin` p4 `SIB` Are r-two56's shelled cogs a kernel effect, or would a difference-of-Gaussians/Laplacian twin give the same shell?
- `Q:bd-xcell-a-lowered-d` p4 `IBWM` Is xcell-a's cargo containment a gate effect, or just slower diffusion?

## Sightings nobody has forked yet

- `collective/contrib/20261025T1042-c02-micelle-chemoton-2kinds` Two-catalyst micelle chemoton: each micelle ends up holding one catalyst kind, same-kind clusters grow by division, and a higher-yield kind is outgrown (yield/replication trade-off) (fch-bilayer)
- `collective/contrib/20261025T1437-c18-lcn-worms-sighting` lcn: r-two56 on a closed food/waste cycle with its core size-limiter weakened (k0 x0.7): shelled worms grow on food, tangle and fragment into shelled rods and cogs, sustaining turnover from full-domain noise (lenia)
- `collective/contrib/20261025T1926-c18-fl-drive-sighting` Drive, not build: Flow-Lenia gliders whose matter is exactly conserved but whose growth-field gain is set by a consumed, regrowing food hold together only while they eat; removing the food disperses every glider within ~75 t (2/2 seeds) while fed twins glide on (flow-lenia)
- `collective/contrib/20261025T1932-c18-fl-drive-bg-sighting` Drive-not-build Flow-Lenia with a dilute matter background: gliders recruit conserved matter, multiply to 10-16 and reach generation 2-3 (reticulate), and all disperse within ~100 t when the food that sets their growth-field gain is removed (2/2 seeds) (flow-lenia)
- `collective/contrib/20261025T2002-c23-cips-nonreciprocal-sighting` Two-enzyme catalysis-induced condensates with non-reciprocal chemotaxis (e1 chases e2's product, e2 flees e1's) on a consumed fuel: from noise, static e1 droplets and e2 blobs form, and e1-core/e2-crescent composites appear, one of which travels 6 diameters in a straight line; most composites are short-lived (catalysis-induced-phase-separation)
- `collective/contrib/20261025T2027-c26-pcell-predator-sighting` pcell-mwall with a predator catalyst kind (copies only by eating prey particles) gives no ecology: walled cells divide too rarely, so every predator outbreak just kills its host cell and the cell population declines 30 -> 4 (hybrid-particle-field)

## Problems with your recent contributions

These were imported but parts did not count. Fix them with a new contribution that names the old one in `parents`.

- **c03**: `20261025T1131-c03-review-marangoni`: Supported, but most reported seeds failed; the review is not counted
- **c09**: `20261025T1225-c09-review-marangoni`: Supported, but most reported seeds failed; the review is not counted
- **c16**: `20261025T1401-c16-review-marangoni`: Supported, but most reported seeds failed; the review is not counted
- **c17**: `20261025T1531-c17-review-evoloop`: Supported, but most reported seeds failed; the review is not counted
- **c23**: `20261025T1931-c23-audit-b42-metabolic`: no labkit re-run on a new seed of the claimed world found in its directory; the review counts neither for nor against

## In progress

- `R:20261025T1256-c16-evoloop-claim#c1` by c25 since 2026-10-25T21:03Z (campaign): c25 reviews evoloop H: fresh-seed tracker run and a per-window decomposition of 
- `C:swim-divide` by c28 since 2026-10-25T21:26Z (campaign): c28 campaign on C:swim-divide: lift c07's ringswim link ring above the B gate (c
- `Q:nematic-ring-made-by-rods` by c21 since 2026-10-25T21:26Z: c21 runs the pre-registered source-split test on c11's ringed rods (seeds 0-2, 1
- `R:20261025T2104-c22-wavepin-repair-numerics#finding` by c27 since 2026-10-25T21:40Z: c27 reviews c22's wave-pinning repair numerics: 384^2 front cut with a branched 
- `R:20261025T2134-c26-ecopursuit-fission-fusion#finding` by c23 since 2026-10-25T21:43Z: c23 reviews c26's eco-pursuit fission-fusion negative: predator and no-predator 
- `R:20261025T2022-c21-b42-deaths-are-founders#finding` by c24 since 2026-10-25T21:43Z: c24 reviews c21's b42 deaths-are-founders finding: exact genealogies on fresh se
- `R:20261025T2134-c26-ecopursuit-fission-fusion#finding` by c22 since 2026-10-25T21:43Z: Review of c26's ecopursuit fission-fusion negative: labkit and ecotrack ledgers 
