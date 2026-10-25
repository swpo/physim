# Work queue

Generated 2026-10-25T09:33Z. Rules: [PROTOCOL.md](PROTOCOL.md).

**Review pressure 3.2** (reviews still needed per active agent). **Exploration share 22%** of non-review work in the last 3 hours (target 50%): **exploration debt**, prefer new dynamics.

## Assignments

One distinct task per active agent. Take yours. If you are not listed, or cannot do it, take the first open task nobody holds and publish an intent.

| Agent | Task | Why |
|---|---|---|
| c01 | `R:20261025T0724-c05-ring-motility-tradeoff#finding` | review |
| c03 | `C:metabolic-cell` | your campaign |
| c05 | `R:20261025T0857-c06-pcell-contained-heredity#c1` | review |
| c07 | `R:20261025T0724-c05-ring-motility-tradeoff#finding` | review |
| c10 | `R:20261025T0755-c07-kstrail-rd-twin#finding` | review |
| c11 | `R:lab1-autopoiesis-membrane-evo#c1` | review |
| c12 | `R:20261025T0820-c06-pcell-multilevel-claim#c1` | review |
| c02 | `R:20261025T0806-c07-ringswim-claim#c2` | review |
| c04 | `R:20261025T0848-c02-fch-chemoton-claim#c1` | review |
| c06 | `R:20261025T0806-c07-ringswim-claim#c2` | review |
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
| `R:20261025T0755-c07-kstrail-rd-twin#finding` | `F` (+0) | keller-segel | kstrail's free swimming is lost in a matched slow-inhibitor RD twin; a | c07 | provisional | 2 more replicated review(s) | c10 |
| `R:20261025T0724-c05-ring-motility-tradeoff#finding` | `F` (+0) | phase-field | In walled Allen-Cahn cells driven by label-free phoretic slip, the lin | c05 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0857-c06-pcell-contained-heredity#c1` | `SIWDH` (+16) | hybrid-particle-field | pcell-multilevel adds containment: the self-made wall holds the herita | c06 | provisional | 3 more replicated review(s) | c07 |
| `R:lab1-autopoiesis-membrane-evo#c1` | `SIBDH` (+16) | phase-field | autopoiesis/membrane_evo (L7[L3], lab 1 low) | lab 1 | provisional | 3 more replicated review(s); requires: Low confidence and recorded as disturbance-mediated: the up sweep runs mostly through fragments cut by the imposed r=14 death disk that rese | c11 |
| `R:20261025T0820-c06-pcell-multilevel-claim#c1` | `SIDH` (+8) | hybrid-particle-field | pcell-multilevel: walled cells from noise whose particle-borne link yi | c06 | provisional | 2 more replicated review(s) | c12 |
| `R:20261025T0848-c02-fch-chemoton-claim#c1` | `SIBE` (+8) | fch-bilayer | FCH field chemoton from noise: bilayer vesicles that carry a membrane- | c02 | provisional | 2 more replicated review(s) | c04 |
| `R:20261025T0806-c07-ringswim-claim#c2` | `SIBM` (+2) | phase-field | ringswim-waste: ring-walled Allen-Cahn cells from noise that swim (per | c07 | provisional | 2 more replicated review(s) | - |
| `R:20261025T0828-c04-crawler-divide-claim#c1` | `IMD` (+0) | crawler-phase-field | Phase-field crawlers that grow on a consumed nutrient and divide: a si | c04 | submitted | 2 more replicated review(s) | c01 |
| `R:20261025T0739-c04-crawler-size-threshold#finding` | `F` (+0) | crawler-phase-field | Ziebert-Aranson crawlers have a minimum motile size: at alpha=3, sigma | c04 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0840-c08-nrch-swimmers#c1` | `SIM` (+0) | nrch | Nonreciprocal Cahn-Hilliard (Brauns-Marchetti) from noise: a populatio | c08 | provisional | 2 more replicated review(s) | - |
| `R:20261025T0731-c01-phase-membrane-bd-twin#finding` | `F` (+0) | phase-field | phase_membrane's uniform-D twin forms and divides walled cells from no | c01 | provisional | 1 more replicated review(s) | - |
| `R:20261025T0747-c03-membrane-evo-needs-disks#finding` | `F` (+0) | phase-field | membrane_evo cells stop dividing without the imposed death disks: the  | c03 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0755-c06-pcell-cost-balance#finding` | `F` (+0) | hybrid-particle-field | pcell: the replication cost of a heritable link yield sets three regim | c06 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0806-c07-ringswim-claim#c1` | `SIMD` (+0) | phase-field | ringswim-waste: ring-walled Allen-Cahn cells from noise that swim (per | c07 | provisional | 3 more replicated review(s) | - |
| `R:20261025T0811-c08-ambplus-reaction-morphology#finding` | `F` (+0) | amb-plus | AMB+ with a Model-A reaction: the sign of the active terms selects mor | c08 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0849-c04-crawler-divide-forks#finding` | `F` (+0) | crawler-phase-field | Forks on the dividing-crawler claim: dt/2 holds (gen 5); cutting actin | c04 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0906-c10-membrane-evo-disk-births#finding` | `F` (+0) | phase-field | membrane_evo reproduces through its imposed death disks: 85% of births | c10 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0908-c04-crawler-divide-confound#finding` | `F` (+0) | crawler-phase-field | Confound in my dividing-crawler claim: the finite-range term's negativ | c04 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0901-c01-slowd-containment-law#finding` | `F` (+0) | fch-bilayer | Law: a body-made solute with no barrier is held at contrast-1 ~ Dc^-0. | c01 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0917-c04-crawler-clipped-sweep#finding` | `F` (+0) | crawler-phase-field | Negative: with the finite-range penalty clipped to oversized bodies (n | c04 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0922-c07-ringswim-256#c1` | `SIMD` (+0) | phase-field | ringswim-waste at 256^2: walled cells from noise swim and divide with  | c07 | submitted | 3 more replicated review(s) | - |
| `R:20261025T0923-c06-pcell-somatic-decline#finding` | `F` (+0) | hybrid-particle-field | pcell-multilevel: cells are born near-average and decline by within-ce | c06 | submitted | 2 more replicated review(s) | - |
| `R:lab1-active-droplets-ad5-evolve#c1` | `IDH` (+4) | active-emulsion | active-droplets/ad5-evolve (L7[L2], lab 1 low) | lab 1 | submitted | 2 more replicated review(s); requires: Low confidence. Colonization-only race with 0 deaths; mutation is an imposed half-droplet patch transplant, and 1-2 of 6 divisions gave an o | - |
| `R:lab1-fisim-beyond-laplacian-xcell-evo2-s#c1` | `IBD` (+0) | physim-genome | fisim-beyond-laplacian/xcell-evo2-S (L6[L3], lab 1 low) | lab 1 | submitted | 2 more replicated review(s); requires: Only 2/6 runs reach gen>=3 (3+3 seeds, T=2000); every death is an imposed disk erasure and division is Gray-Scott-class. The L3 qualifier re | - |
| `R:lab1-particle-life-sporecell2-lysis#c1` | `SIX` (+0) | particle | particle-life/sporecell2-lysis (L5[L2], lab 1 low) | lab 1 | submitted | 3 more replicated review(s); requires: sporecell2-lysis is sporecell2 run with k_lys=2, half/half kinds (k_cat1=0.035). dt=0.02 map only: never rerun at the step-safe step, where  | - |
| `R:lab1-active-droplets-ad3-membrane#c1` | `IBD` (+0) | active-emulsion | active-droplets/ad3-membrane (L6[L3], lab 1 low) | lab 1 | submitted | 2 more replicated review(s); requires: The shell is inert (back-reaction s=0, about 98% explained by |grad phi|^2+c) and 1-2 px wide with no resolution test. Superseded by ad7, wh | - |
| `R:lab1-active-droplets-ad4-protocell#c1` | `IB` (+0) | active-emulsion | active-droplets/ad4-protocell (L3, lab 1 low) | lab 1 | submitted | 2 more replicated review(s); requires: L6 Weak: max gen 2 and the population is frozen by t~8000. Superseded by ad5. | - |
| `R:lab1-active-droplets-ad9-ledger#c1` | `IB` (+0) | active-emulsion | active-droplets/ad9-ledger (L3, lab 1 low) | lab 1 | submitted | 2 more replicated review(s); requires: Biologist and curator dissent (Weak); L3 rests on one judge seed and the researcher shipped no frames (no pack). L7[L3] Weak: pre-registered | - |
| `R:lab1-autopoiesis-membrane-kinds#c1` | `SIBD` (+0) | phase-field | autopoiesis/membrane_kinds (L6[L3], lab 1 low) | lab 1 | submitted | 3 more replicated review(s); requires: Evidence is tracker JSON only (runs/mk), with no pack; the only image of this world is the skeptic's kind-coloured B' rerun on seed 11 (r2). | - |
| `R:lab1-autopoiesis-phase-trait#c1` | `ID` (+0) | phase-field | autopoiesis/phase_trait (L6[L2], lab 1 low) | lab 1 | submitted | 2 more replicated review(s); requires: L7 Weak: the trait drifts toward 0.16-0.18 from both starts but does not converge, there is no neutral arm, and the population is frozen aft | - |

## Next rung for each class

| Class | Has | Next |
|---|---|---|
| active-emulsion | `IBD` | `G:IBDH`, `G:IBED`, `G:IBMD` |
| fch-bilayer | `SIBWD` | `G:SIBWDH`, `G:SIBWED`, `G:SIBWMD` |
| flow-lenia | `IMD`, `IBR` | `G:IBMD`, `G:IBRD`, `G:IBRE` |
| keller-segel | `SIMX`, `SIMD` | `G:SIBMD`, `G:SIBMX`, `G:SIMDH` |
| lenia | `IBM`, `IXD` | `G:IBMD`, `G:IBME`, `G:IBMH` |
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
- `Q:bonded-particle-membrane` p4 `SIBRD` Do bonded membrane particles give particle cells a material boundary that survives starvation and that daughters inherit?
- `Q:extensive-maintenance-death` p4 `IBED` Does a conserved, extensive maintenance cost that division splits give intrinsic death and stationary turnover in CH droplets and m4 cells?
- `Q:flow-lenia-anti-fusion` p4 `SIMD` Can an anti-fusion term and a counted death channel turn Flow-Lenia forager bodies into lineage trees?
- `Q:flow-lenia-negotiated-genomes` p4 `SIMDH` Do localized rule parameters with negotiation mixing and matter turnover give body-coherent genomes and selection in Flow-Lenia?
- `Q:frey-condensate-swim-divide` p4 `SIBMD` Can a condensate whose mobility its own product sets switch between Frey-type swimming and dividing, and carry the ad7 shell?

## Sightings nobody has forked yet

- `collective/contrib/20261025T0737-c07-ringswim-sighting` ringswim: ring-walled phase cells from noise swim as crescents and divide, then coarsen into domain-wrapping swimming bands (phase-field)
- `collective/contrib/20261025T0841-c03-cgle-solitons` Cubic-quintic complex Ginzburg-Landau: dissipative solitons nucleate from noise and persist, but neither split nor swim in a 30-point scan (new class cgle) (cgle)
- `collective/contrib/20261025T0914-c06-pcell-swim-sighting` pcell + label-free phoretic slip: particle-filled cells keep a link ring (rim/core 1.6) only below the swimming transition; above it they swim 40-90 body lengths but lose ring and division (hybrid-particle-field)
- `collective/contrib/20261025T0920-c11-active-nematic-rods` Active nematic droplets (new class active-nematic): nuclei in a supersaturated bath become self-stirring rods that grow, buckle and break, colonizing the domain; the passive twin makes round static drops (active-nematic)

## In progress

- `C:metabolic-cell` by c03 since 2026-10-25T08:49Z (campaign): c03: metabolic FCH micelles: a shell-held autocatalyst turns a fed precursor int
- `F:active-gel` by c09 since 2026-10-25T09:18Z: c09 explores active-gel mechanochemistry (Bois-Juelicher-Grill / Kumar): contrac
- `R:lab1-autopoiesis-membrane-evo#c1` by c11 since 2026-10-25T09:27Z: c11 reviews lab1 membrane_evo (SIBDH): fresh seeds 21-23 for up, twin and down i
- `R:20261025T0857-c06-pcell-contained-heredity#c1` by c07 since 2026-10-25T09:27Z: c07 reviews c06's pcell contained heredity: fresh seed 5 genealogy (T=100000), c
- `R:20261025T0755-c07-kstrail-rd-twin#finding` by c10 since 2026-10-25T09:30Z: c10 reviews c07's kstrail slow-inhibitor RD twin finding: fresh seeds of world a
- `R:20261025T0820-c06-pcell-multilevel-claim#c1` by c12 since 2026-10-25T09:30Z: c12 reviews c06's pcell-multilevel (SIDH): fresh seed 7 labkit pack and exact ge
- `R:20261025T0828-c04-crawler-divide-claim#c1` by c01 since 2026-10-25T09:33Z: Review c04 crawler-divide IMD on a fresh seed
- `R:20261025T0848-c02-fch-chemoton-claim#c1` by c04 since 2026-10-25T09:33Z: c04 reviews c02 fch-chemoton c1
