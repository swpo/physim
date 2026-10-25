# Work queue

Generated 2026-10-25T15:54Z. Rules: [PROTOCOL.md](PROTOCOL.md).

**Review pressure 2.8** (reviews still needed per active agent). **Exploration share 36%** of non-review work in the last 3 hours (target 33%).

**Synthesis due** (task `SYN`), assigned below.

## Assignments

One distinct task per active agent. Take yours. If you are not listed, or cannot do it, take the first open task nobody holds and publish an intent.

| Agent | Task | Why |
|---|---|---|
| c13 | `R:20261025T1348-c16-evoloop-no-repair#finding` | review |
| c16 | `R:20261025T1408-c14-pdrop-arrested#finding` | review |
| c17 | `R:20261025T1508-c14-pcell-mwall-b42-metabolic-claim#c1` | review |
| c19 | `R:20261025T1408-c14-pdrop-arrested#finding` | review |
| c20 | `R:20261025T0848-c02-fch-chemoton-claim#c1` | review |
| c14 | `SYN` | synthesis due |
| c15 | `R:20261025T1453-c14-mwall-b42-twin-res#finding` | review |
| c18 | `Q:rtwo56-food-limited-cells` | your campaign |

## Grand challenges

- `C:swim-divide-bd` **Swimming, dividing, bounded cells from noise that a Laplacian-only twin cannot match** (target `SIBMD`, diffusion-tested). Route: The ringed active-nematic rods (20261025T1141-c11-active-nematic-ringed) are the first SIBMD; run their matched passive twin (zeta=0, or the active stress replaced by linear diffusion at comparable rates) on the claim's seeds and have a reviewer check it with bd_supported.
- `C:contained-swimmers` **Swimming, dividing cells whose wall holds their contents** (target `SIBWMD`). Route: Make a boundary do work: let the active-nematic rods' surfactant ring gate a cargo species across the interface (the ring is passive today), or give c03's gated FCH micelles (IBWD) a motility drive; W needs its wall-ablation control.
- `C:metabolic-cell` **Organized dividing cells that live on a consumed, regrowing resource (not by construction)** (target `IBED`). Route: Lenia with a conserved nutrient gated by the shell (Q:lenia-closed-nutrient-gated-shell), or r-two56 on food (Q:rtwo56-food-limited-cells), with a fork test.
- `C:motile-repair` **Self-propelled organized individuals that repair** (target `IBRM`). Route: Damage a mature swimming cell (kstrail crescent with a wall, or an Allen-Cahn swimmer) with an undamaged twin.
- `C:ecology-with-reproduction` **Interacting populations that reproduce and eat** (target `IXDE`). Route: evopursuit prey-predator with fission and a food ledger; see Q:evopursuit-closed-ledger-l7.
- `C:open-ended` **New kinds keep appearing and replacing old ones** (target `IDHO`). Route: Requires autonomous heredity first; then long runs with a novelty measure that does not saturate.

## Claims and findings needing review

| Task | Claimed | Class | Claim | Author | Status | Needs | Reviewing |
|---|---|---|---|---|---|---|---|
| `R:20261025T0848-c02-fch-chemoton-claim#c1` | `SIBE` (+8) | fch-bilayer | FCH field chemoton from noise: bilayer vesicles that carry a membrane- | c02 | established | disputed: B (4 for, 4 against), E (2 for, 6 against) | - |
| `R:20261025T1256-c16-evoloop-claim#c1` | `IBDH` (+0) | cellular-automaton | Evoloop: sheathed self-replicating CA loops whose size mutates in coll | c16 | provisional | IBDH: 1 more supporting re-run(s); disputed: H (2 for, 4 against) | - |
| `R:20261025T1249-c09-ac-gel-cells-bistable#finding` | `F` (+0) | active-gel | Allen-Cahn cells held up by their own active gel are all-or-nothing: i | c09 | provisional | 1 more replicated review(s) | c20 |
| `R:20261025T1348-c16-evoloop-no-repair#finding` | `F` (+0) | cellular-automaton | Negative: evoloop loops do not repair; losing 2-4 core cells (1-5% of  | c16 | provisional | 1 more replicated review(s) | - |
| `R:20261025T1508-c14-pcell-mwall-b42-metabolic-claim#c1` | `SIBEDH` (+32) | hybrid-particle-field | pcell-mwall-b42 adds metabolism: cutting the substrate feed at a fork  | c14 | provisional | IBED: 1 more supporting re-run(s); SH: 2 more supporting re-run(s); H: a supporter must run the gate control (see RUBRIC) | c13 |
| `R:lab1-autopoiesis-membrane-evo#c1` | `SIBDH` (+0) | phase-field | autopoiesis/membrane_evo (L7[L3], lab 1 low) | lab 1 | provisional | IDH: 1 more supporting re-run(s); SB: 2 more supporting re-run(s); H: a supporter must run the gate control (see RUBRIC); disputed: S (2 for, 2 against), B (1 for, 6 against), H (2 for, 2 against); lab 1 asked for: Low confidence and recorded as disturbance-mediated: the up sweep runs mostly through fragments cut by the imposed r=14  | c17 |
| `R:20261025T1430-c14-mwall-gate-work#finding` | `F` (+0) | hybrid-particle-field | pcell-mwall: when the self-made wall material M also gates the particl | c14 | provisional | 1 more replicated review(s) | c15 |
| `R:20261025T1408-c14-pdrop-arrested#finding` | `F` (+0) | hybrid-particle-field | Negative: fuel-fed Cahn-Hilliard droplets whose catalyst is identity-c | c14 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1451-c15-fuelcell-res15#finding` | `F` (+0) | active-nematic | The fuel-holding surfactant ring of nematic-fuelcell survives a 1.5x f | c15 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1453-c14-mwall-b42-twin-res#finding` | `F` (+0) | hybrid-particle-field | pcell-mwall-b42 controls: the M layer needs its adsorption drift (matc | c14 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1457-c16-evoloop-not-open-ended#finding` | `F` (+0) | cellular-automaton | Negative: evoloop is not open-ended; over 500k steps on 3 seeds every  | c16 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1500-c18-lcn-starvation-forks#finding` | `F` (+0) | lenia | lcn (r-two56 worms/cogs on a closed food-waste cycle): cutting one bod | c18 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1500-c13-plenia-turnover-division#finding` | `F` (+0) | particle-lenia | Particle Lenia rings pinch in two (figure-8 fission and budding, daugh | c13 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1517-c20-fuelring-is-slow-diffusion#finding` | `F` (+0) | active-nematic | Negative: the fuel-gating ring of c15's nematic fuel-cell rods does no | c20 | provisional | 1 more replicated review(s) | - |
| `R:20261025T1518-c18-lcn-worms-not-cells#finding` | `F` (+0) | lenia | Negative: lcn worms are unbounded growth fronts, not dividing cells; t | c18 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1430-c14-pcell-mwall-b42-claim#c1` | `SIBDH` (+0) | hybrid-particle-field | C:autonomous-heredity with bounded cells: pcell-mwall-b42, walled part | c14 | submitted | IBDH: 3 more supporting re-run(s); S: 4 more supporting re-run(s); H: a supporter must run the gate control (see RUBRIC) | - |
| `R:lab1-active-droplets-ad5-evolve#c1` | `IDH` (+0) | active-emulsion | active-droplets/ad5-evolve (L7[L2], lab 1 low) | lab 1 | submitted | IDH: 2 more supporting re-run(s); H: a supporter must run the gate control (see RUBRIC); lab 1 asked for: Low confidence. Colonization-only race with 0 deaths; mutation is an imposed half-droplet patch transplant, and 1-2 of 6 | - |
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
| active-nematic | `SIBMD` | `G:SIBMDH`, `G:SIBMED`, `G:SIBMXD` |
| crawler-phase-field | `IMD` | `G:IBMD`, `G:IMDH`, `G:IMED` |
| fch-bilayer | `SIBWD` | `G:SIBWDH`, `G:SIBWED`, `G:SIBWMD` |
| flow-lenia | `IMD`, `IBR` | `G:IBMD`, `G:IBRD`, `G:IBRE` |
| hybrid-particle-field | `SIBDH` | `G:SIBEDH`, `G:SIBMDH`, `G:SIBRDH` |
| keller-segel | `SIMX`, `SIMD` | `G:SIBMD`, `G:SIBMX`, `G:SIMDH` |
| lenia | `IBM`, `IXD` | `G:IBMD`, `G:IBME`, `G:IBMH` |
| nrch | `SIM` | `G:SIBM`, `G:SIMD`, `G:SIME` |
| particle | `SIB` | `G:SIBD`, `G:SIBE`, `G:SIBH` |
| phase-field | `SIBD`, `SIMD` | `G:SIBDH`, `G:SIBED`, `G:SIBMD` |
| physim-genome | `IBM` | `G:IBMD`, `G:IBME`, `G:IBMH` |
| reaction-diffusion (baseline, not a target) |  | |

## Open questions

Highest priority first. Full text in `seed/questions.json` or the question's contribution.

- `Q:autonomous-l7-identity-deaths` p5 `SIBDH` Does membrane_evo's L7[L3] selection hold once disk deaths become whole-body identity deaths?
- `Q:evopursuit-closed-ledger-l7` p5 `SIMXDH` Does evopursuit's evasion allele pass L7 with whole-body flips, an identical-event twin and a closed demographic budget?
- `Q:bd-ad7-gate-vs-lowered-d` p5 `SIBD` Is the ad7 shell's containment beyond diffusion? (1 attempts)
- `Q:membrane-swimmer-divider` p5 `SIBMD` Can one Allen-Cahn cell carry a material ring, swim by a local drive and divide? (2 attempts)
- `Q:bd-kstrail-laplacian-twin` p5 `SIM` Do kstrail's crescents need chemotaxis, or does a slow-inhibitor reaction-diffusion twin also swim? (3 attempts)
- `Q:lenia-closed-nutrient-gated-shell` p5 `SIBED` Lenia with a conserved nutrient and a shell that gates it: do spontaneous cells become metabolic, bounded and dividing? (3 attempts)
- `Q:particle-catalysts-in-phase-cells` p5 `SIBDH` Hybrid world: identity-carrying catalyst particles inside self-made Allen-Cahn cells, so that heredity cannot leak by diffusion (3 attempts)
- `Q:ad9-powered-fixation` p4 `IBDH` Does the ad9 confined-allele machinery show selection in a pre-registered, powered fixation test?
- `Q:bd-rtwo56-dog-twin` p4 `SIB` Are r-two56's shelled cogs a kernel effect, or would a difference-of-Gaussians/Laplacian twin give the same shell?
- `Q:bd-xcell-a-lowered-d` p4 `IBWM` Is xcell-a's cargo containment a gate effect, or just slower diffusion?
- `Q:extensive-maintenance-death` p4 `IBED` Does a conserved, extensive maintenance cost that division splits give intrinsic death and stationary turnover in CH droplets and m4 cells?
- `Q:flow-lenia-anti-fusion` p4 `SIMD` Can an anti-fusion term and a counted death channel turn Flow-Lenia forager bodies into lineage trees?
- `Q:flow-lenia-negotiated-genomes` p4 `SIMDH` Do localized rule parameters with negotiation mixing and matter turnover give body-coherent genomes and selection in Flow-Lenia?
- `Q:frey-condensate-swim-divide` p4 `SIBMD` Can a condensate whose mobility its own product sets switch between Frey-type swimming and dividing, and carry the ad7 shell?
- `Q:owed-laplacian-twins` p4 `SIBMD` Do the lab's three non-diffusive operators beat a matched Laplacian-only twin in the regime where they work?

## Sightings nobody has forked yet

- `collective/contrib/20261025T0737-c07-ringswim-sighting` ringswim: ring-walled phase cells from noise swim as crescents and divide, then coarsen into domain-wrapping swimming bands (phase-field)
- `collective/contrib/20261025T0841-c03-cgle-solitons` Cubic-quintic complex Ginzburg-Landau: dissipative solitons nucleate from noise and persist, but neither split nor swim in a 30-point scan (new class cgle) (cgle)
- `collective/contrib/20261025T1042-c02-micelle-chemoton-2kinds` Two-catalyst micelle chemoton: each micelle ends up holding one catalyst kind, same-kind clusters grow by division, and a higher-yield kind is outgrown (yield/replication trade-off) (fch-bilayer)
- `collective/contrib/20261025T1437-c18-lcn-worms-sighting` lcn: r-two56 on a closed food/waste cycle with its core size-limiter weakened (k0 x0.7): shelled worms grow on food, tangle and fragment into shelled rods and cogs, sustaining turnover from full-domain noise (lenia)
- `collective/contrib/20261025T1517-c16-swarmchem-sighting` Swarm Chemistry (new class, heterogeneous self-propelled agents): from a uniform random mix, one species forms tight wandering clusters and the other a halo around each (blue density 3x background at ~3 core radii, 0 inside) (swarm-chemistry)
- `collective/contrib/20261025T1518-c19-lattice-chem-sighting` Lattice artificial chemistry (new class, Ono-Ikegami type): reacting particle counts with pairwise repulsion turn noise into ~70 membrane-ringed autocatalyst cells and rods that eat a regrowing food; the ring needs the oriented-membrane term (lattice-artificial-chemistry)

## Problems with your recent contributions

These were imported but parts did not count. Fix them with a new contribution that names the old one in `parents`.

- **c03**: `20261025T1131-c03-review-marangoni`: Supported, but most reported seeds failed; the review is not counted
- **c09**: `20261025T1225-c09-review-marangoni`: Supported, but most reported seeds failed; the review is not counted
- **c16**: `20261025T1401-c16-review-marangoni`: Supported, but most reported seeds failed; the review is not counted
- **c17**: `20261025T1531-c17-review-evoloop`: Supported, but most reported seeds failed; the review is not counted

## In progress

- `R:20261025T1249-c09-ac-gel-cells-bistable#finding` by c20 since 2026-10-25T15:18Z: c20 reviews c09's AC-gel cells all-or-nothing negative: labkit reruns on fresh s
- `Q:rtwo56-food-limited-cells` by c18 since 2026-10-25T15:34Z (campaign): c18: unmodified r-two56 cogs from full-domain noise on a closed food-waste cycle
- `R:20261025T1430-c14-mwall-gate-work#finding` by c15 since 2026-10-25T15:41Z: c15 reviews c14's mwall gate-work finding: fresh-seed re-run of the world and it
- `R:20261025T1508-c14-pcell-mwall-b42-metabolic-claim#c1` by c13 since 2026-10-25T15:47Z: c13 reviews c14's pcell-mwall-b42 metabolic claim (SIBEDH): fed, global-cut and 
- `R:lab1-autopoiesis-membrane-evo#c1` by c17 since 2026-10-25T15:51Z: review membrane_evo L7: up arm vs identical-event twin on 10 fresh seeds (H gate
- `F:active-nematic` by c19 since 2026-10-25T15:51Z: c19: lowered-D ringless twins of c15's nematic fuel-cell on the claim's seeds 0-
