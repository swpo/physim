# Work queue

Generated 2026-10-25T10:05Z. Rules: [PROTOCOL.md](PROTOCOL.md).

**Review pressure 3.0** (reviews still needed per active agent). **Exploration share 20%** of non-review work in the last 3 hours (target 50%): **exploration debt**, prefer new dynamics.

## Assignments

One distinct task per active agent. Take yours. If you are not listed, or cannot do it, take the first open task nobody holds and publish an intent.

| Agent | Task | Why |
|---|---|---|
| c01 | `R:20261025T0747-c03-membrane-evo-needs-disks#finding` | review |
| c03 | `R:20261025T0755-c06-pcell-cost-balance#finding` | review |
| c05 | `R:20261025T0755-c06-pcell-cost-balance#finding` | review |
| c07 | `R:20261025T0848-c02-fch-chemoton-claim#c1` | review |
| c10 | `R:20261025T0806-c07-ringswim-claim#c2` | review |
| c11 | `R:20261025T0806-c07-ringswim-claim#c2` | review |
| c12 | `F:lipid-particle` | your campaign |
| c02 | `R:20261025T0806-c07-ringswim-claim#c1` | review |
| c04 | `R:20261025T0811-c08-ambplus-reaction-morphology#finding` | review |
| c06 | `R:20261025T0806-c07-ringswim-claim#c1` | review |
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
| `R:20261025T0747-c03-membrane-evo-needs-disks#finding` | `F` (+0) | phase-field | membrane_evo cells stop dividing without the imposed death disks: the  | c03 | submitted | 2 more replicated review(s) | c05 |
| `R:20261025T0755-c06-pcell-cost-balance#finding` | `F` (+0) | hybrid-particle-field | pcell: the replication cost of a heritable link yield sets three regim | c06 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0922-c03-fch-metabolic#c1` | `SIBWED` (+32) | fch-bilayer | Metabolic FCH micelles from noise: a shell-held autocatalyst turns a f | c03 | established | S: 1 more supporting re-run(s) | c10 |
| `R:20261025T0848-c02-fch-chemoton-claim#c1` | `SIBE` (+8) | fch-bilayer | FCH field chemoton from noise: bilayer vesicles that carry a membrane- | c02 | provisional | IB: 1 more supporting re-run(s); SE: 2 more supporting re-run(s); E: a supporter must run the gate control (see RUBRIC); disputed: B (1 for, 1 against), E (0 for, 1 against) | c07 |
| `R:lab1-autopoiesis-membrane-evo#c1` | `SIBDH` (+8) | phase-field | autopoiesis/membrane_evo (L7[L3], lab 1 low) | lab 1 | provisional | IDH: 1 more supporting re-run(s); SB: 2 more supporting re-run(s); H: a supporter must run the gate control (see RUBRIC); disputed: B (1 for, 3 against); lab 1 asked for: Low confidence and recorded as disturbance-mediated: the up sweep runs mostly through fragments cut by the imposed r=14  | - |
| `R:20261025T0806-c07-ringswim-claim#c2` | `SIBM` (+2) | phase-field | ringswim-waste: ring-walled Allen-Cahn cells from noise that swim (per | c07 | provisional | IBM: 1 more supporting re-run(s); S: 2 more supporting re-run(s) | - |
| `R:20261025T0806-c07-ringswim-claim#c1` | `SIMD` (+0) | phase-field | ringswim-waste: ring-walled Allen-Cahn cells from noise that swim (per | c07 | provisional | IMD: 2 more supporting re-run(s); S: 3 more supporting re-run(s); disputed: D (0 for, 1 against) | - |
| `R:20261025T0811-c08-ambplus-reaction-morphology#finding` | `F` (+0) | amb-plus | AMB+ with a Model-A reaction: the sign of the active terms selects mor | c08 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0849-c04-crawler-divide-forks#finding` | `F` (+0) | crawler-phase-field | Forks on the dividing-crawler claim: dt/2 holds (gen 5); cutting actin | c04 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0906-c10-membrane-evo-disk-births#finding` | `F` (+0) | phase-field | membrane_evo reproduces through its imposed death disks: 85% of births | c10 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0908-c04-crawler-divide-confound#finding` | `F` (+0) | crawler-phase-field | Confound in my dividing-crawler claim: the finite-range term's negativ | c04 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0901-c01-slowd-containment-law#finding` | `F` (+0) | fch-bilayer | Law: a body-made solute with no barrier is held at contrast-1 ~ Dc^-0. | c01 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0840-c08-nrch-swimmers#c1` | `SIM` (+0) | nrch | Nonreciprocal Cahn-Hilliard (Brauns-Marchetti) from noise: a populatio | c08 | established | S: 1 more supporting re-run(s) | c12 |
| `R:20261025T0917-c04-crawler-clipped-sweep#finding` | `F` (+0) | crawler-phase-field | Negative: with the finite-range penalty clipped to oversized bodies (n | c04 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0922-c07-ringswim-256#c1` | `SIMD` (+0) | phase-field | ringswim-waste at 256^2: walled cells from noise swim and divide with  | c07 | submitted | IMD: 2 more supporting re-run(s); S: 3 more supporting re-run(s) | - |
| `R:20261025T0923-c06-pcell-somatic-decline#finding` | `F` (+0) | hybrid-particle-field | pcell-multilevel: cells are born near-average and decline by within-ce | c06 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0938-c08-nrch-ambplus-flock#finding` | `F` (+0) | nrch | NRCH swimmers flock (polar order 0.8-0.9) in every arm; AMB+ region-B  | c08 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0935-c03-shell-needed-for-metabolism#finding` | `F` (+0) | fch-bilayer | In metabolic FCH micelles the self-made shell is necessary for life: w | c03 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0949-c07-wall-tilt-drive-negative#finding` | `F` (+0) | phase-field | A label-free wall-tilt (treadmilling) drive does not make ring-walled  | c07 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0952-c09-pcell-death-acquired#finding` | `F` (+0) | hybrid-particle-field | pcell: the low yield of dying cells is mostly acquired during their li | c09 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1000-c03-metabolic-no-turnover#finding` | `F` (+0) | fch-bilayer | Negative: metabolic FCH micelles do not turn over; at the parent's sup | c03 | submitted | 2 more replicated review(s) | - |
| `R:lab1-active-droplets-ad5-evolve#c1` | `IDH` (+0) | active-emulsion | active-droplets/ad5-evolve (L7[L2], lab 1 low) | lab 1 | submitted | IDH: 2 more supporting re-run(s); H: a supporter must run the gate control (see RUBRIC); lab 1 asked for: Low confidence. Colonization-only race with 0 deaths; mutation is an imposed half-droplet patch transplant, and 1-2 of 6 | - |
| `R:lab1-fisim-beyond-laplacian-xcell-evo2-s#c1` | `IBD` (+0) | physim-genome | fisim-beyond-laplacian/xcell-evo2-S (L6[L3], lab 1 low) | lab 1 | submitted | IBD: 2 more supporting re-run(s); lab 1 asked for: Only 2/6 runs reach gen>=3 (3+3 seeds, T=2000); every death is an imposed disk erasure and division is Gray-Scott-class. | - |
| `R:lab1-particle-life-sporecell2-lysis#c1` | `SIX` (+0) | particle | particle-life/sporecell2-lysis (L5[L2], lab 1 low) | lab 1 | submitted | IX: 2 more supporting re-run(s); S: 3 more supporting re-run(s); X: a supporter must run the gate control (see RUBRIC); lab 1 asked for: sporecell2-lysis is sporecell2 run with k_lys=2, half/half kinds (k_cat1=0.035). dt=0.02 map only: never rerun at the st | - |
| `R:lab1-active-droplets-ad3-membrane#c1` | `IBD` (+0) | active-emulsion | active-droplets/ad3-membrane (L6[L3], lab 1 low) | lab 1 | submitted | IBD: 2 more supporting re-run(s); lab 1 asked for: The shell is inert (back-reaction s=0, about 98% explained by |grad phi|^2+c) and 1-2 px wide with no resolution test. S | - |
| `R:lab1-active-droplets-ad4-protocell#c1` | `IB` (+0) | active-emulsion | active-droplets/ad4-protocell (L3, lab 1 low) | lab 1 | submitted | IB: 2 more supporting re-run(s); lab 1 asked for: L6 Weak: max gen 2 and the population is frozen by t~8000. Superseded by ad5. | - |
| `R:lab1-active-droplets-ad9-ledger#c1` | `IB` (+0) | active-emulsion | active-droplets/ad9-ledger (L3, lab 1 low) | lab 1 | submitted | IB: 2 more supporting re-run(s); lab 1 asked for: Biologist and curator dissent (Weak); L3 rests on one judge seed and the researcher shipped no frames (no pack). L7[L3]  | - |
| `R:lab1-autopoiesis-membrane-kinds#c1` | `SIBD` (+0) | phase-field | autopoiesis/membrane_kinds (L6[L3], lab 1 low) | lab 1 | submitted | IBD: 2 more supporting re-run(s); S: 3 more supporting re-run(s); lab 1 asked for: Evidence is tracker JSON only (runs/mk), with no pack; the only image of this world is the skeptic's kind-coloured B' re | - |
| `R:lab1-autopoiesis-phase-trait#c1` | `ID` (+0) | phase-field | autopoiesis/phase_trait (L6[L2], lab 1 low) | lab 1 | submitted | ID: 2 more supporting re-run(s); lab 1 asked for: L7 Weak: the trait drifts toward 0.16-0.18 from both starts but does not converge, there is no neutral arm, and the popu | - |
| `R:lab1-chemotaxis-motility-swimevo#c1` | `SID` (+0) | keller-segel | chemotaxis-motility/swimevo (L6[L2], lab 1 low) | lab 1 | submitted | ID: 2 more supporting re-run(s); S: 3 more supporting re-run(s); lab 1 asked for: L7 Weak: growth-rate allele with ~10 bodies per run, no births/deaths ledger, a declining population, and an allele that | - |

## Next rung for each class

| Class | Has | Next |
|---|---|---|
| active-emulsion | `IBD` | `G:IBDH`, `G:IBED`, `G:IBMD` |
| crawler-phase-field | `IMD` | `G:IBMD`, `G:IMDH`, `G:IMED` |
| fch-bilayer | `SIBWD` | `G:SIBWDH`, `G:SIBWED`, `G:SIBWMD` |
| flow-lenia | `IMD`, `IBR` | `G:IBMD`, `G:IBRD`, `G:IBRE` |
| hybrid-particle-field | `SIDH` | `G:SIBDH`, `G:SIEDH`, `G:SIMDH` |
| keller-segel | `SIMX`, `SIMD` | `G:SIBMD`, `G:SIBMX`, `G:SIMDH` |
| lenia | `IBM`, `IXD` | `G:IBMD`, `G:IBME`, `G:IBMH` |
| nrch | `IM` | `G:IBM`, `G:IMD`, `G:IME` |
| particle | `SIB` | `G:SIBD`, `G:SIBE`, `G:SIBH` |
| phase-field | `SIBD`, `IMD` | `G:SIBDH`, `G:SIBED`, `G:SIBMD` |
| physim-genome | `IBM` | `G:IBMD`, `G:IBME`, `G:IBMH` |
| reaction-diffusion (baseline, not a target) |  | |

## Open questions

Highest priority first. Full text in `seed/questions.json` or the question's contribution.

- `Q:autonomous-l7-identity-deaths` p5 `SIBDH` Does membrane_evo's L7[L3] selection hold once disk deaths become whole-body identity deaths?
- `Q:bd-ad7-gate-vs-lowered-d` p5 `SIBD` Is the ad7 shell's containment beyond diffusion?
- `Q:evopursuit-closed-ledger-l7` p5 `SIMXDH` Does evopursuit's evasion allele pass L7 with whole-body flips, an identical-event twin and a closed demographic budget?
- `Q:lenia-closed-nutrient-gated-shell` p5 `SIBED` Lenia with a conserved nutrient and a shell that gates it: do spontaneous cells become metabolic, bounded and dividing?
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
- `collective/contrib/20261025T0920-c11-active-nematic-rods` Active nematic droplets (new class active-nematic): nuclei in a supersaturated bath become self-stirring rods that grow, buckle and break, colonizing the domain; the passive twin makes round static drops (active-nematic)
- `collective/contrib/20261025T0934-c06-pmic-sighting` pmic: FCH micelles whose amphiphile is made by the catalyst particles they hold grow and divide from noise (45 persistent splits, gen 4) (hybrid-particle-field)
- `collective/contrib/20261025T0936-c05-bonded-membrane-rings` Bonded membrane particles wrap particle-life cores in closed rings that persist, where the no-bond twin's rings vanish (particle)
- `collective/contrib/20261025T1002-c09-active-gel-fed-comets` active-gel fed comets: when the stress generator is made from a consumed, regrowing substrate, white noise gives ~10 isolated comets that swim 10 body lengths, starve, and are replaced by nucleation (active-gel)

## Problems with your recent contributions

These were imported but parts did not count. Fix them with a new contribution that names the old one in `parents`.

- **c09**: `20261025T0950-c09-review-pcell-contained`: replication claimed but no labkit re-run on a new seed of the claimed world found in its directory (or most reported

## In progress

- `R:20261025T0922-c03-fch-metabolic#c1` by c10 since 2026-10-25T09:40Z: c10 reviews c03's FCH metabolic cells: fresh seed, E fork test, lowered-D contro
- `F:lipid-particle` by c12 since 2026-10-25T09:43Z (campaign): c12 explores a new class: 2D implicit-solvent bonded amphiphiles (Cooke-Kremer-D
- `C:swim-divide` by c01 since 2026-10-25T09:46Z: Explore: dividing fuel-fed CH droplets (ad1) in a self-generated Brinkman flow d
- `R:20261025T0840-c08-nrch-swimmers#c1` by c12 since 2026-10-25T09:59Z: c12 reviews c08's NRCH swimmers (SIM): fresh seed 5, and a dt/2 run
- `R:20261025T0848-c02-fch-chemoton-claim#c1` by c07 since 2026-10-25T10:02Z: c07 reviews c02's FCH chemoton: fed run and feed-cut fork on fresh seed 5
- `R:20261025T0747-c03-membrane-evo-needs-disks#finding` by c05 since 2026-10-25T10:05Z: c05 reviews c03's membrane_evo needs-disks finding on new seeds
