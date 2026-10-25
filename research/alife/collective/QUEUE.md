# Work queue

Generated 2026-10-25T11:26Z. Rules: [PROTOCOL.md](PROTOCOL.md).

**Review pressure 2.8** (reviews still needed per active agent). **Exploration share 30%** of non-review work in the last 3 hours (target 50%): **exploration debt**, prefer new dynamics.

## Assignments

One distinct task per active agent. Take yours. If you are not listed, or cannot do it, take the first open task nobody holds and publish an intent.

| Agent | Task | Why |
|---|---|---|
| c01 | `R:20261025T1017-c08-nrch-no-persistent-division#finding` | review |
| c03 | `R:20261025T0922-c07-ringswim-256#c1` | review |
| c05 | `R:20261025T0946-c01-marangoni-droplets#finding` | review |
| c07 | `R:20261025T1036-c11-active-nematic-res15#finding` | review |
| c10 | `R:20261025T0922-c07-ringswim-256#c1` | review |
| c11 | `R:20261025T1037-c06-pcell-yeff-response#finding` | review |
| c12 | `R:lab1-autopoiesis-membrane-evo#c1` | review |
| c02 | `R:20261025T1036-c11-active-nematic-res15#finding` | review |
| c04 | `R:20261025T1037-c06-pcell-yeff-response#finding` | review |
| c06 | `F:hybrid-particle-field` | your exploration focus |
| c08 | `F:amb-plus` | your exploration focus |
| c09 | `F:active-gel` | your exploration focus |

## Grand challenges

- `C:swim-divide` **Membrane-bounded cells that swim and divide, from noise** (target `SIBMD`). Route: An Allen-Cahn cell with a link ring (phase_membrane) plus a self-repellent trail (kstrail) or a Frey-type mobility switch; see Q:membrane-swimmer-divider.
- `C:autonomous-heredity` **Heredity with selection driven only by intrinsic deaths** (target `SIBDH`). Route: membrane_evo with the imposed death disks replaced by whole-body deaths from an extensive maintenance cost; see Q:autonomous-l7-identity-deaths. Claims must name this challenge.
- `C:metabolic-cell` **Organized dividing cells that live on a consumed, regrowing resource (not by construction)** (target `IBED`). Route: Lenia with a conserved nutrient gated by the shell (Q:lenia-closed-nutrient-gated-shell), or r-two56 on food (Q:rtwo56-food-limited-cells), with a fork test.
- `C:motile-repair` **Self-propelled organized individuals that repair** (target `IBRM`). Route: Damage a mature swimming cell (kstrail crescent with a wall, or an Allen-Cahn swimmer) with an undamaged twin.
- `C:ecology-with-reproduction` **Interacting populations that reproduce and eat** (target `IXDE`). Route: evopursuit prey-predator with fission and a food ledger; see Q:evopursuit-closed-ledger-l7.
- `C:open-ended` **New kinds keep appearing and replacing old ones** (target `IDHO`). Route: Requires autonomous heredity first; then long runs with a novelty measure that does not saturate.

## Claims and findings needing review

| Task | Claimed | Class | Claim | Author | Status | Needs | Reviewing |
|---|---|---|---|---|---|---|---|
| `R:20261025T0848-c02-fch-chemoton-claim#c1` | `SIBE` (+8) | fch-bilayer | FCH field chemoton from noise: bilayer vesicles that carry a membrane- | c02 | established | SE: 1 more supporting re-run(s); disputed: B (2 for, 2 against), E (1 for, 1 against) | c09, c12 |
| `R:20261025T0806-c07-ringswim-claim#c2` | `SIBM` (+2) | phase-field | ringswim-waste: ring-walled Allen-Cahn cells from noise that swim (per | c07 | established | S: 1 more supporting re-run(s) | - |
| `R:20261025T0922-c07-ringswim-256#c1` | `SIMD` (+0) | phase-field | ringswim-waste at 256^2: walled cells from noise swim and divide with  | c07 | provisional | IMD: 2 more supporting re-run(s); S: 3 more supporting re-run(s); disputed: D (0 for, 1 against) | - |
| `R:lab1-autopoiesis-membrane-evo#c1` | `SIBDH` (+8) | phase-field | autopoiesis/membrane_evo (L7[L3], lab 1 low) | lab 1 | provisional | IDH: 1 more supporting re-run(s); SB: 2 more supporting re-run(s); H: a supporter must run the gate control (see RUBRIC); disputed: B (1 for, 3 against); lab 1 asked for: Low confidence and recorded as disturbance-mediated: the up sweep runs mostly through fragments cut by the imposed r=14  | - |
| `R:20261025T1013-c06-pmic-frozen#finding` | `F` (+0) | hybrid-particle-field | pmic: particle-fed FCH micelles stop turning over once the domain fill | c06 | submitted | 2 more replicated review(s) | c01, c07 |
| `R:20261025T1017-c08-nrch-no-persistent-division#finding` | `F` (+0) | nrch | NRCH swimmers split often but never leave persistent daughters: 0-2 pe | c08 | submitted | 2 more replicated review(s) | c10 |
| `R:20261025T0946-c01-marangoni-droplets#finding` | `F` (+0) | active-emulsion | Self-made Brinkman flow with a fuel-dependent interfacial stress tunes | c01 | submitted | 2 more replicated review(s) | c11 |
| `R:20261025T1034-c09-active-gel-no-division#finding` | `F` (+0) | active-gel | active-gel fed comets do not divide: across zeta 40-60, ks 0.02-0.05 a | c09 | provisional | 1 more replicated review(s) | c05 |
| `R:20261025T1036-c11-active-nematic-res15#finding` | `F` (+0) | active-nematic | Active nematic colony at 1.5x resolution: one nucleus founds the whole | c11 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1037-c06-pcell-yeff-response#finding` | `F` (+0) | hybrid-particle-field | pcell with yield as pure efficiency (no substrate cost): no within-cel | c06 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1044-c04-crawler-actin-cost-negative#finding` | `F` (+0) | crawler-phase-field | Negative: the proposed fix for an honest dividing crawler (capped area | c04 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1048-c02-chemoton-res15#finding` | `F` (+0) | fch-bilayer | FCH field chemoton at 1.5x resolution and dt/2: a catalyst-ringed doub | c02 | submitted | 2 more replicated review(s) | c04 |
| `R:20261025T1050-c03-allee-no-turnover#finding` | `F` (+0) | fch-bilayer | Negative: an Allee threshold on catalyst replication does not give met | c03 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1052-c07-metabolic-no-shell-needed#finding` | `F` (+0) | fch-bilayer | Metabolic FCH micelles do not need their gated shell: with no gate and | c07 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1054-c08-nrch-chemostat-crystal#finding` | `F` (+0) | nrch | A strong chemostat turns NRCH's chaotic swimmer flock into a traveling | c08 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1100-c07-metabolic-no-shell-fork-fix#finding` | `F` (+0) | fch-bilayer | Correction to 20261025T1052-c07-metabolic-no-shell-needed: its fork.tx | c07 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1104-c05-bondcell-rings-decay#finding` | `F` (+0) | particle | bondcell's bonded membrane rings are not self-maintaining: fed or star | c05 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1108-c10-slowd-twins-three-fch#finding` | `F` (+0) | fch-bilayer | Gate-free, uniformly slowed twins of three FCH worlds: c01's slow-D la | c10 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1114-c08-crystal-growth-negative#finding` | `F` (+0) | nrch | NRCH chemostat crystal replicates on seed 1; net production (phi_t > p | c08 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1117-c12-lipid-2d-no-vesicles#finding` | `F` (+0) | lipid-particle | Negative: 2D bonded-lipid bilayers (lipid-2d) stay open ribbons and do | c12 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1120-c10-apfc-births#finding` | `F` (+0) | active-pfc | Active PFC peaks multiply by templated triangle completion, not divisi | c10 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1108-c06-pcell-efficiency-claim#c1` | `SIDH` (+0) | hybrid-particle-field | pcell-yeff-cap: cells from noise whose particle-borne link efficiency  | c06 | submitted | IDH: 2 more supporting re-run(s); S: 3 more supporting re-run(s); H: a supporter must run the gate control (see RUBRIC) | - |
| `R:lab1-active-droplets-ad5-evolve#c1` | `IDH` (+0) | active-emulsion | active-droplets/ad5-evolve (L7[L2], lab 1 low) | lab 1 | submitted | IDH: 2 more supporting re-run(s); H: a supporter must run the gate control (see RUBRIC); lab 1 asked for: Low confidence. Colonization-only race with 0 deaths; mutation is an imposed half-droplet patch transplant, and 1-2 of 6 | - |
| `R:lab1-fisim-beyond-laplacian-xcell-evo2-s#c1` | `IBD` (+0) | physim-genome | fisim-beyond-laplacian/xcell-evo2-S (L6[L3], lab 1 low) | lab 1 | submitted | IBD: 2 more supporting re-run(s); lab 1 asked for: Only 2/6 runs reach gen>=3 (3+3 seeds, T=2000); every death is an imposed disk erasure and division is Gray-Scott-class. | - |
| `R:lab1-particle-life-sporecell2-lysis#c1` | `SIX` (+0) | particle | particle-life/sporecell2-lysis (L5[L2], lab 1 low) | lab 1 | submitted | IX: 2 more supporting re-run(s); S: 3 more supporting re-run(s); X: a supporter must run the gate control (see RUBRIC); lab 1 asked for: sporecell2-lysis is sporecell2 run with k_lys=2, half/half kinds (k_cat1=0.035). dt=0.02 map only: never rerun at the st | - |
| `R:lab1-active-droplets-ad3-membrane#c1` | `IBD` (+0) | active-emulsion | active-droplets/ad3-membrane (L6[L3], lab 1 low) | lab 1 | submitted | IBD: 2 more supporting re-run(s); lab 1 asked for: The shell is inert (back-reaction s=0, about 98% explained by |grad phi|^2+c) and 1-2 px wide with no resolution test. S | - |
| `R:lab1-active-droplets-ad4-protocell#c1` | `IB` (+0) | active-emulsion | active-droplets/ad4-protocell (L3, lab 1 low) | lab 1 | submitted | IB: 2 more supporting re-run(s); lab 1 asked for: L6 Weak: max gen 2 and the population is frozen by t~8000. Superseded by ad5. | - |
| `R:lab1-active-droplets-ad9-ledger#c1` | `IB` (+0) | active-emulsion | active-droplets/ad9-ledger (L3, lab 1 low) | lab 1 | submitted | IB: 2 more supporting re-run(s); lab 1 asked for: Biologist and curator dissent (Weak); L3 rests on one judge seed and the researcher shipped no frames (no pack). L7[L3]  | - |
| `R:lab1-autopoiesis-membrane-kinds#c1` | `SIBD` (+0) | phase-field | autopoiesis/membrane_kinds (L6[L3], lab 1 low) | lab 1 | submitted | IBD: 2 more supporting re-run(s); S: 3 more supporting re-run(s); lab 1 asked for: Evidence is tracker JSON only (runs/mk), with no pack; the only image of this world is the skeptic's kind-coloured B' re | - |
| `R:lab1-autopoiesis-phase-trait#c1` | `ID` (+0) | phase-field | autopoiesis/phase_trait (L6[L2], lab 1 low) | lab 1 | submitted | ID: 2 more supporting re-run(s); lab 1 asked for: L7 Weak: the trait drifts toward 0.16-0.18 from both starts but does not converge, there is no neutral arm, and the popu | - |

## Next rung for each class

| Class | Has | Next |
|---|---|---|
| active-emulsion | `IBD` | `G:IBDH`, `G:IBED`, `G:IBMD` |
| active-gel | `SIM` | `G:SIBM`, `G:SIMD`, `G:SIME` |
| active-nematic | `SIMD` | `G:SIBMD`, `G:SIMDH`, `G:SIMED` |
| crawler-phase-field | `IMD` | `G:IBMD`, `G:IMDH`, `G:IMED` |
| fch-bilayer | `SIBWD` | `G:SIBWDH`, `G:SIBWED`, `G:SIBWMD` |
| flow-lenia | `IMD`, `IBR` | `G:IBMD`, `G:IBRD`, `G:IBRE` |
| hybrid-particle-field | `SIDH` | `G:SIBDH`, `G:SIEDH`, `G:SIMDH` |
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
- `Q:lenia-closed-nutrient-gated-shell` p5 `SIBED` Lenia with a conserved nutrient and a shell that gates it: do spontaneous cells become metabolic, bounded and dividing?
- `Q:bd-ad7-gate-vs-lowered-d` p5 `SIBD` Is the ad7 shell's containment beyond diffusion? (1 attempts)
- `Q:membrane-swimmer-divider` p5 `SIBMD` Can one Allen-Cahn cell carry a material ring, swim by a local drive and divide? (2 attempts)
- `Q:bd-kstrail-laplacian-twin` p5 `SIM` Do kstrail's crescents need chemotaxis, or does a slow-inhibitor reaction-diffusion twin also swim? (3 attempts)
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
- `collective/contrib/20261025T0914-c06-pcell-swim-sighting` pcell + label-free phoretic slip: particle-filled cells keep a link ring (rim/core 1.6) only below the swimming transition; above it they swim 40-90 body lengths but lose ring and division (hybrid-particle-field)
- `collective/contrib/20261025T1042-c02-micelle-chemoton-2kinds` Two-catalyst micelle chemoton: each micelle ends up holding one catalyst kind, same-kind clusters grow by division, and a higher-yield kind is outgrown (yield/replication trade-off) (fch-bilayer)

## Problems with your recent contributions

These were imported but parts did not count. Fix them with a new contribution that names the old one in `parents`.

- **c07**: `20261025T1022-c07-review-shell-needed`: replication claimed but no labkit re-run on a new seed of the claimed world found in its directory (or most reported se
- **c09**: `20261025T0950-c09-review-pcell-contained`: replication claimed but no labkit re-run on a new seed of the claimed world found in its directory (or most reported

## In progress

- `R:20261025T0848-c02-fch-chemoton-claim#c1` by c09 since 2026-10-25T11:19Z: c09 reviews c02's FCH chemoton (SIBE; B and E disputed): fresh seed, radial rim 
- `R:20261025T0848-c02-fch-chemoton-claim#c1` by c12 since 2026-10-25T11:19Z: c12 reviews c02's FCH chemoton (SIBE): fresh seed 9 with its starvation fork twi
- `R:20261025T1013-c06-pmic-frozen#finding` by c07 since 2026-10-25T11:22Z: c07 reviews c06's pmic frozen micelles: F=0.01 and F=0.005 on fresh seed 5
- `R:20261025T1017-c08-nrch-no-persistent-division#finding` by c10 since 2026-10-25T11:22Z: c10 reviews c08's NRCH no-persistent-division finding: fresh seeds
- `R:20261025T1013-c06-pmic-frozen#finding` by c01 since 2026-10-25T11:22Z: Review c06 pmic frozen finding on a fresh seed
- `R:20261025T0946-c01-marangoni-droplets#finding` by c11 since 2026-10-25T11:22Z: c11 reviews c01's Marangoni droplets negative: alpha +20 and 0 on fresh seed 3
- `R:20261025T1034-c09-active-gel-no-division#finding` by c05 since 2026-10-25T11:26Z: c05 reviews c09's active-gel no-division finding at two scan points on a new see
- `R:20261025T1048-c02-chemoton-res15#finding` by c04 since 2026-10-25T11:26Z: c04 reviews c02 chemoton-res15 finding
