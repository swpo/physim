# Work queue

Generated 2026-10-25T07:52Z. Rules: [PROTOCOL.md](PROTOCOL.md).

**Review pressure 2.2** (reviews still needed per active agent). **Exploration share 25%** of non-review work in the last 3 hours (target 50%): **exploration debt**, prefer new dynamics.

## Assignments

One distinct task per active agent. Take yours. If you are not listed, or cannot do it, take the first open task nobody holds and publish an intent.

| Agent | Task | Why |
|---|---|---|
| c01 | `R:20261025T0726-c03-fch-protocell#c1` | review |
| c02 | `R:lab1-autopoiesis-membrane-evo#c1` | review |
| c03 | `C:inherited-contents` | your campaign |
| c04 | `R:lab1-autopoiesis-membrane-evo#c1` | review |
| c05 | `R:20261025T0726-c03-fch-protocell#c1` | review |
| c06 | `C:autonomous-heredity` | your campaign |
| c07 | `R:20261025T0648-c06-pcell-yield-selection#finding` | review |
| c08 | `R:lab1-autopoiesis-phase-membrane-damage-mature#c1` | review |

## Grand challenges

- `C:swim-divide` **Membrane-bounded cells that swim and divide, from noise** (target `SIBMD`). Route: An Allen-Cahn cell with a link ring (phase_membrane) plus a self-repellent trail (kstrail) or a Frey-type mobility switch; see Q:membrane-swimmer-divider.
- `C:inherited-contents` **Containment that daughters inherit through division** (target `IBWD`). Route: A gated wall (min or harmonic face mobility) that holds a fast species through pinching: xcell-a's gate or ad7's shell on a dividing cell.
- `C:autonomous-heredity` **Heredity with selection driven only by intrinsic deaths** (target `SIBDH`). Route: membrane_evo with the imposed death disks replaced by whole-body deaths from an extensive maintenance cost; see Q:autonomous-l7-identity-deaths. Claims must name this challenge.
- `C:reproduction-beyond-diffusion` **Reproducing organized cells that a Laplacian-only twin cannot match** (target `IBD`, diffusion-tested). Route: Run the owed matched Laplacian twins (Q:owed-laplacian-twins, Q:bd-ad7-gate-vs-lowered-d) on a dividing organized cell.
- `C:metabolic-cell` **Organized dividing cells that live on a consumed, regrowing resource (not by construction)** (target `IBED`). Route: Lenia with a conserved nutrient gated by the shell (Q:lenia-closed-nutrient-gated-shell), or r-two56 on food (Q:rtwo56-food-limited-cells), with a fork test.
- `C:motile-repair` **Self-propelled organized individuals that repair** (target `IBRM`). Route: Damage a mature swimming cell (kstrail crescent with a wall, or an Allen-Cahn swimmer) with an undamaged twin.
- `C:ecology-with-reproduction` **Interacting populations that reproduce and eat** (target `IXDE`). Route: evopursuit prey-predator with fission and a food ledger; see Q:evopursuit-closed-ledger-l7.
- `C:open-ended` **New kinds keep appearing and replacing old ones** (target `IDHO`). Route: Requires autonomous heredity first; then long runs with a novelty measure that does not saturate.

## Claims and findings needing review

| Task | Claimed | Class | Claim | Author | Status | Needs | Reviewing |
|---|---|---|---|---|---|---|---|
| `R:lab1-autopoiesis-membrane-evo#c1` | `SIBDH` (+16) | phase-field | autopoiesis/membrane_evo (L7[L3], lab 1 low) | lab 1 | provisional | 4 more replicated review(s); requires: Low confidence and recorded as disturbance-mediated: the up sweep runs mostly through fragments cut by the imposed r=14 death disk that rese | - |
| `R:20261025T0726-c03-fch-protocell#c1` | `SIBW` (+8) | fch-bilayer | FCH protocells from noise: bilayer vesicles that trap a solute their o | c03 | submitted | 4 more replicated review(s) | - |
| `R:20261025T0648-c06-pcell-yield-selection#finding` | `F` (+0) | hybrid-particle-field | pcell: particle-carried link yield is selected at the cell level, but  | c06 | provisional | 1 more replicated review(s) | - |
| `R:lab1-autopoiesis-phase-membrane-damage-mature#c1` | `SIBR` (+4) | phase-field | autopoiesis/phase_membrane_damage_mature (L4a[L3], lab 1 low) | lab 1 | provisional | 3 more replicated review(s); requires: Replaces the r1 L4a credit (medium under v1). Two of three judges rated it Weak. s1: the target merged into a neighbour. The skeptic's branc | - |
| `R:20261025T0632-c01-kstrail-rd-twin#finding` | `F` (+0) | keller-segel | kstrail's spontaneous swimmers are matched by a Laplacian-only twin: t | c01 | provisional | 1 more replicated review(s) | - |
| `R:20261025T0755-c07-kstrail-rd-twin#finding` | `F` (+0) | keller-segel | kstrail's free swimming is lost in a matched slow-inhibitor RD twin; a | c07 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0711-c06-pcell-cheater-erosion#finding` | `F` (+0) | hybrid-particle-field | pcell: a heritable, costly link yield on the particles erodes inside c | c06 | provisional | 1 more replicated review(s) | - |
| `R:20261025T0658-c01-swimfission-rd-twin#finding` | `F` (+0) | keller-segel | swimfission's Laplacian-only twin swims but rarely divides: 1-3 strict | c01 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0724-c05-ring-motility-tradeoff#finding` | `F` (+0) | phase-field | In walled Allen-Cahn cells driven by label-free phoretic slip, the lin | c05 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0739-c04-crawler-size-threshold#finding` | `F` (+0) | crawler-phase-field | Ziebert-Aranson crawlers have a minimum motile size: at alpha=3, sigma | c04 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0731-c01-phase-membrane-bd-twin#finding` | `F` (+0) | phase-field | phase_membrane's uniform-D twin forms and divides walled cells from no | c01 | submitted | 2 more replicated review(s) | - |
| `R:20261025T0747-c03-membrane-evo-needs-disks#finding` | `F` (+0) | phase-field | membrane_evo cells stop dividing without the imposed death disks: the  | c03 | submitted | 2 more replicated review(s) | - |
| `R:lab1-active-droplets-ad5-evolve#c1` | `IDH` (+4) | active-emulsion | active-droplets/ad5-evolve (L7[L2], lab 1 low) | lab 1 | submitted | 2 more replicated review(s); requires: Low confidence. Colonization-only race with 0 deaths; mutation is an imposed half-droplet patch transplant, and 1-2 of 6 divisions gave an o | - |
| `R:lab1-fisim-beyond-laplacian-xcell-evo2-s#c1` | `IBD` (+0) | physim-genome | fisim-beyond-laplacian/xcell-evo2-S (L6[L3], lab 1 low) | lab 1 | submitted | 2 more replicated review(s); requires: Only 2/6 runs reach gen>=3 (3+3 seeds, T=2000); every death is an imposed disk erasure and division is Gray-Scott-class. The L3 qualifier re | - |
| `R:lab1-particle-life-sporecell2-lysis#c1` | `SIX` (+0) | particle | particle-life/sporecell2-lysis (L5[L2], lab 1 low) | lab 1 | submitted | 3 more replicated review(s); requires: sporecell2-lysis is sporecell2 run with k_lys=2, half/half kinds (k_cat1=0.035). dt=0.02 map only: never rerun at the step-safe step, where  | - |
| `R:lab1-active-droplets-ad3-membrane#c1` | `IBD` (+0) | active-emulsion | active-droplets/ad3-membrane (L6[L3], lab 1 low) | lab 1 | submitted | 2 more replicated review(s); requires: The shell is inert (back-reaction s=0, about 98% explained by |grad phi|^2+c) and 1-2 px wide with no resolution test. Superseded by ad7, wh | - |
| `R:lab1-active-droplets-ad4-protocell#c1` | `IB` (+0) | active-emulsion | active-droplets/ad4-protocell (L3, lab 1 low) | lab 1 | submitted | 2 more replicated review(s); requires: L6 Weak: max gen 2 and the population is frozen by t~8000. Superseded by ad5. | - |
| `R:lab1-active-droplets-ad9-ledger#c1` | `IB` (+0) | active-emulsion | active-droplets/ad9-ledger (L3, lab 1 low) | lab 1 | submitted | 2 more replicated review(s); requires: Biologist and curator dissent (Weak); L3 rests on one judge seed and the researcher shipped no frames (no pack). L7[L3] Weak: pre-registered | - |
| `R:lab1-autopoiesis-membrane-kinds#c1` | `SIBD` (+0) | phase-field | autopoiesis/membrane_kinds (L6[L3], lab 1 low) | lab 1 | submitted | 3 more replicated review(s); requires: Evidence is tracker JSON only (runs/mk), with no pack; the only image of this world is the skeptic's kind-coloured B' rerun on seed 11 (r2). | - |
| `R:lab1-autopoiesis-phase-trait#c1` | `ID` (+0) | phase-field | autopoiesis/phase_trait (L6[L2], lab 1 low) | lab 1 | submitted | 2 more replicated review(s); requires: L7 Weak: the trait drifts toward 0.16-0.18 from both starts but does not converge, there is no neutral arm, and the population is frozen aft | - |
| `R:lab1-chemotaxis-motility-swimevo#c1` | `SID` (+0) | keller-segel | chemotaxis-motility/swimevo (L6[L2], lab 1 low) | lab 1 | submitted | 3 more replicated review(s); requires: L7 Weak: growth-rate allele with ~10 bodies per run, no births/deaths ledger, a declining population, and an allele that wins by constructio | - |
| `R:lab1-fisim-beyond-laplacian-xcell-turn#c1` | `IB` (+0) | physim-genome | fisim-beyond-laplacian/xcell-turn (L3, lab 1 low) | lab 1 | submitted | 2 more replicated review(s); requires: RETRACTED (r2), final: the r1 L6[L3] was withdrawn (not scored Contradicted, but recorded in negatives as retracted). The waste was gated by | - |
| `R:lab1-flow-lenia-fl-forager-mut#c1` | `I` (+0) | flow-lenia | flow-lenia/fl_forager_mut (L2, lab 1 low) | lab 1 | submitted | 2 more replicated review(s); requires: L6 and L7 Weak for fl_forager_mut: the identical-event neutral twin shows as much clade turnover (root share 9% vs 36%), with 177 splits vs  | - |
| `R:lab1-flow-lenia-fl-morph257#c1` | `I` (+0) | flow-lenia | flow-lenia/fl_morph257 (L2, lab 1 low) | lab 1 | submitted | 2 more replicated review(s); requires: One seed; never followed up. L5 (crescents cup rings for 500-650 t), L4b and L6 (20/30 composite divisions give one daughter of each kind) a | - |
| `R:lab1-particle-life-sporecell3-det-twin#c1` | `SI` (+0) | particle | particle-life/sporecell3-det-twin (L2, lab 1 low) | lab 1 | submitted | 3 more replicated review(s); requires: L7[L2] Weak overall: one pair, and the colonization-phase gap (0.36 vs 0.18) is untested. The L5-type matter transfer and conversion is Weak | - |

## Next rung for each class

| Class | Has | Next |
|---|---|---|
| active-emulsion | `IBD` | `G:IBDH`, `G:IBED`, `G:IBMD` |
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

- `collective/contrib/20261025T0702-c03-fch-micelle-fission` FCH micelles fed with amphiphile grow, pinch into dumbbells and split, in synchronized waves, from noise (fch-bilayer)
- `collective/contrib/20261025T0732-c08-ambplus-cluster-phase` AMB+ positive control: reverse Ostwald ripening and an arrested cluster phase from noise (region B, zeta=-1.6, lambda=-0.8) (amb-plus)
- `collective/contrib/20261025T0737-c07-ringswim-sighting` ringswim: ring-walled phase cells from noise swim as crescents and divide, then coarsen into domain-wrapping swimming bands (phase-field)
- `collective/contrib/20261025T0740-c02-chemoton-interim` FCH field chemoton, interim: a planted vesicle lives on its bilayer-held catalyst (no-catalyst twin shrinks away) and grows into lobes, but from noise the catalyst is not encapsulated (fch-bilayer)

## In progress

- `C:autonomous-heredity` by c06 since 2026-10-25T07:33Z (campaign): c06: claim S,I,D,H on pcell-yield: a heritable particle link yield rises under s
- `R:lab1-autopoiesis-phase-membrane#c1` by c01 since 2026-10-25T07:49Z: Review phase_membrane SIBD on fresh seed 7 with the uniform-D twin as the matche
- `C:inherited-contents` by c03 since 2026-10-25T07:52Z (campaign): c03: FCH bodies that keep a self-made cargo through division: micelle fission wi
