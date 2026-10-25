# Work queue

Generated 2026-10-25T17:52Z. Rules: [PROTOCOL.md](PROTOCOL.md).

**Review pressure 3.2** (reviews still needed per active agent). **Exploration share 28%** of non-review work in the last 3 hours (target 33%): **exploration debt**, prefer new dynamics.

**Synthesis due** (task `SYN`), assigned below.

**Literature check due** (task `LIT`, see PROTOCOL.md), assigned below.

## Assignments

One distinct task per active agent. Take yours. If you are not listed, or cannot do it, take the first open task nobody holds and publish an intent.

| Agent | Task | Why |
|---|---|---|
| c13 | `A:20261025T1412-c15-nematic-fuelcell-claim#c1` | audit of a large claim |
| c16 | `SYN` | synthesis due |
| c17 | `A:20261025T0810-c01-fch-uptake-cargo#c1` | audit of a large claim |
| c19 | `R:20261025T1748-c18-flshell2-metabolic-cell-claim#c1` | review |
| c20 | `R:20261025T1748-c18-flshell2-metabolic-cell-claim#c1` | review |
| c21 | `R:20261025T1508-c14-pcell-mwall-b42-metabolic-claim#c1` | review |
| c23 | `Q:cips-fuel-limited-condensates` | your campaign |
| c24 | `R:20261025T0848-c02-fch-chemoton-claim#c1` | review |
| c14 | `R:20261025T1733-c20-neural-comets-metabolic-claim#c1` | review |
| c15 | `R:20261025T1430-c14-pcell-mwall-b42-claim#c1` | review |
| c18 | `R:20261025T1256-c16-evoloop-claim#c1` | review |
| c22 | `R:20261025T0848-c02-fch-chemoton-claim#c1` | review |
## Audits due

Independent audits of large claims, at most 2 at a time (PROTOCOL.md, Audit).

- `A:20261025T1412-c15-nematic-fuelcell-claim#c1` `SIBD` active-nematic: Active nematic rods from noise whose self-made surfactant ring does work: it holds the fue
- `A:20261025T0810-c01-fch-uptake-cargo#c1` `SID` fch-bilayer: FCH micelles from noise concentrate a uniformly supplied solute 140-170x and keep it throu


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
| `R:20261025T1508-c14-pcell-mwall-b42-metabolic-claim#c1` | `SIBEDH` (+32) | hybrid-particle-field | pcell-mwall-b42 adds metabolism: cutting the substrate feed at a fork  | c14 | established | H: a supporter must run the gate control (see RUBRIC) | - |
| `R:20261025T0848-c02-fch-chemoton-claim#c1` | `SIBE` (+8) | fch-bilayer | FCH field chemoton from noise: bilayer vesicles that carry a membrane- | c02 | established | disputed: B (4 for, 7 against), E (2 for, 8 against) | - |
| `R:20261025T1256-c16-evoloop-claim#c1` | `IBDH` (+0) | cellular-automaton | Evoloop: sheathed self-replicating CA loops whose size mutates in coll | c16 | established | disputed: H (3 for, 4 against) | c18 |
| `R:20261025T1517-c20-fuelring-is-slow-diffusion#finding` | `F` (+0) | active-nematic | Negative: the fuel-gating ring of c15's nematic fuel-cell rods does no | c20 | provisional | 1 more replicated review(s) | c19 |
| `R:20261025T1430-c14-pcell-mwall-b42-claim#c1` | `SIBDH` (+0) | hybrid-particle-field | C:autonomous-heredity with bounded cells: pcell-mwall-b42, walled part | c14 | established | H: a supporter must run the gate control (see RUBRIC) | - |
| `R:20261025T1748-c18-flshell2-metabolic-cell-claim#c1` | `IBMED` (+18) | flow-lenia | C:metabolic-cell attempt (IBMED, flow-lenia): food-eating Flow-Lenia g | c18 | submitted | IBMED: 3 more supporting re-run(s); E: a supporter must run the gate control (see RUBRIC) | - |
| `R:20261025T1733-c20-neural-comets-metabolic-claim#c1` | `SIMED` (+16) | neural-field | Neural-field comets live on a consumed, regrowing resource: cutting th | c20 | submitted | IMED: 3 more supporting re-run(s); S: 4 more supporting re-run(s); E: a supporter must run the gate control (see RUBRIC) | - |
| `R:lab1-autopoiesis-membrane-evo#c1` | `SIBDH` (+0) | phase-field | autopoiesis/membrane_evo (L7[L3], lab 1 low) | lab 1 | established | B: 2 more supporting re-run(s); H: a supporter must run the gate control (see RUBRIC); disputed: B (1 for, 8 against); lab 1 asked for: Low confidence and recorded as disturbance-mediated: the up sweep runs mostly through fragments cut by the imposed r=14  | - |
| `R:20261025T1721-c20-neural-comets-depression-claim#c1` | `SIMD` (+0) | neural-field | Neural-field comets with synaptic depression: from noise, a gas of 30- | c20 | established | S: 1 more supporting re-run(s) | - |
| `R:20261025T1621-c18-rtwo56-food-cogs-res15#finding` | `F` (+0) | lenia | lcn-cog at 1.5x resolution (R=15, 288^2): cogs still form from noise w | c18 | provisional | 1 more replicated review(s) | - |
| `R:20261025T1639-c19-lattice-chem-no-division#finding` | `F` (+0) | lattice-artificial-chemistry | Negative: the lattice-chem membrane cells (Ono-Ikegami type) do not di | c19 | provisional | 1 more replicated review(s) | - |
| `R:20261025T1641-c17-chemoton-decay-source#finding` | `F` (+0) | fch-bilayer | Negative (artefact): in the FCH field chemoton the amphiphile 'decay'  | c17 | submitted | 2 more replicated review(s) | c20 |
| `R:20261025T1655-c14-catalyst-rods-no-selection#finding` | `F` (+0) | hybrid-particle-field | Negative: in the catalyst-rods world the particle-borne production rat | c14 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1656-c19-lattice-chem-ring-passive#finding` | `F` (+0) | lattice-artificial-chemistry | Negative: the lattice-chem membrane ring is passive; removing it (orie | c19 | submitted | 2 more replicated review(s) | c20 |
| `R:20261025T1700-c15-fuelcell-motility-negative#finding` | `F` (+0) | active-nematic | Negative: the fuel-cell nematic rods do not become swimmers by stiffer | c15 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1703-c18-cog-gate-is-slow-diffusion#finding` | `F` (+0) | lenia | Gating food and waste through r-two56's shell lets a cog outlive a cut | c18 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1713-c15-fuelcell-outslow-twin#finding` | `F` (+0) | active-nematic | Ringless twin of nematic-fuelcell with fuel slowed only outside the ro | c15 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1713-c20-neural-comets-no-fission#finding` | `F` (+0) | neural-field | Negative: neural-field comets do not divide by themselves; at theta=0. | c20 | provisional | 1 more replicated review(s) | - |
| `R:20261025T1658-c19-lattice-chem-gated-wall#finding` | `F` (+0) | lattice-artificial-chemistry | Negative: a membrane that gates the autocatalyst's hops (Ono-Ikegami-l | c19 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1725-c15-outslow-seed1-dose#finding` | `F` (+0) | active-nematic | Outside-slow ringless twin of nematic-fuelcell, third seed and a weake | c15 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1727-c18-flshell-push-no-antifusion#finding` | `F` (+0) | flow-lenia | Negative: a set-point shell that pushes matter back inside (F -= gamma | c18 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1729-c16-swarmchem-18-no-division#finding` | `F` (+0) | swarm-chemistry | Negative: Swarm Chemistry recipe 3/18's blue-coated bodies do not repr | c16 | submitted | 2 more replicated review(s) | - |
| `R:20261025T1751-c20-neural-comets-jitter#finding` | `F` (+0) | neural-field | Robustness of the neural-field comet gas: +-10% in kd, tr, g and theta | c20 | submitted | 2 more replicated review(s) | - |
| `R:lab1-active-droplets-ad5-evolve#c1` | `IDH` (+0) | active-emulsion | active-droplets/ad5-evolve (L7[L2], lab 1 low) | lab 1 | submitted | IDH: 2 more supporting re-run(s); H: a supporter must run the gate control (see RUBRIC); lab 1 asked for: Low confidence. Colonization-only race with 0 deaths; mutation is an imposed half-droplet patch transplant, and 1-2 of 6 | - |
| `R:lab1-fisim-beyond-laplacian-xcell-evo2-s#c1` | `IBD` (+0) | physim-genome | fisim-beyond-laplacian/xcell-evo2-S (L6[L3], lab 1 low) | lab 1 | submitted | IBD: 2 more supporting re-run(s); lab 1 asked for: Only 2/6 runs reach gen>=3 (3+3 seeds, T=2000); every death is an imposed disk erasure and division is Gray-Scott-class. | - |
| `R:lab1-particle-life-sporecell2-lysis#c1` | `SIX` (+0) | particle | particle-life/sporecell2-lysis (L5[L2], lab 1 low) | lab 1 | submitted | IX: 2 more supporting re-run(s); S: 3 more supporting re-run(s); X: a supporter must run the gate control (see RUBRIC); lab 1 asked for: sporecell2-lysis is sporecell2 run with k_lys=2, half/half kinds (k_cat1=0.035). dt=0.02 map only: never rerun at the st | - |
| `R:lab1-active-droplets-ad3-membrane#c1` | `IBD` (+0) | active-emulsion | active-droplets/ad3-membrane (L6[L3], lab 1 low) | lab 1 | submitted | IBD: 2 more supporting re-run(s); lab 1 asked for: The shell is inert (back-reaction s=0, about 98% explained by |grad phi|^2+c) and 1-2 px wide with no resolution test. S | - |
| `R:lab1-active-droplets-ad4-protocell#c1` | `IB` (+0) | active-emulsion | active-droplets/ad4-protocell (L3, lab 1 low) | lab 1 | submitted | IB: 2 more supporting re-run(s); lab 1 asked for: L6 Weak: max gen 2 and the population is frozen by t~8000. Superseded by ad5. | - |
| `R:lab1-active-droplets-ad9-ledger#c1` | `IB` (+0) | active-emulsion | active-droplets/ad9-ledger (L3, lab 1 low) | lab 1 | submitted | IB: 2 more supporting re-run(s); lab 1 asked for: Biologist and curator dissent (Weak); L3 rests on one judge seed and the researcher shipped no frames (no pack). L7[L3]  | - |
| `R:lab1-autopoiesis-membrane-kinds#c1` | `SIBD` (+0) | phase-field | autopoiesis/membrane_kinds (L6[L3], lab 1 low) | lab 1 | submitted | IBD: 2 more supporting re-run(s); S: 3 more supporting re-run(s); lab 1 asked for: Evidence is tracker JSON only (runs/mk), with no pack; the only image of this world is the skeptic's kind-coloured B' re | - |

## Next rung for each class

| Class | Has | Next |
|---|---|---|
| active-emulsion | `IBD` | `G:IBDH`, `G:IBED`, `G:IBMD` |
| active-gel | `SIM` | `G:SIBM`, `G:SIMD`, `G:SIME` |
| active-nematic | `SIBD`, `SIMD` | `G:SIBDH`, `G:SIBED`, `G:SIBMD` |
| cellular-automaton | `ID` | `G:IBD`, `G:IDH`, `G:IED` |
| crawler-phase-field | `IMD` | `G:IBMD`, `G:IMDH`, `G:IMED` |
| fch-bilayer | `SIBWD` | `G:SIBWDH`, `G:SIBWED`, `G:SIBWMD` |
| flow-lenia | `IMD`, `IBR` | `G:IBMD`, `G:IBRD`, `G:IBRE` |
| hybrid-particle-field | `SIBDH` | `G:SIBEDH`, `G:SIBMDH`, `G:SIBRDH` |
| keller-segel | `SIMX`, `SIMD` | `G:SIBMD`, `G:SIBMX`, `G:SIMDH` |
| lenia | `IBM`, `IXD` | `G:IBMD`, `G:IBME`, `G:IBMH` |
| neural-field | `IMD` | `G:IBMD`, `G:IMDH`, `G:IMED` |
| nrch | `SIM` | `G:SIBM`, `G:SIMD`, `G:SIME` |
| particle | `SIB` | `G:SIBD`, `G:SIBE`, `G:SIBH` |
| phase-field | `SIBD`, `SIMD` | `G:SIBDH`, `G:SIBED`, `G:SIBMD` |
| physim-genome | `IBM` | `G:IBMD`, `G:IBME`, `G:IBMH` |
| reaction-diffusion (baseline, not a target) |  | |

## Open questions

Highest priority first. Full text in `seed/questions.json` or the question's contribution.

- `Q:autonomous-l7-identity-deaths` p5 `SIBDH` Does membrane_evo's L7[L3] selection hold once disk deaths become whole-body identity deaths?
- `Q:evopursuit-closed-ledger-l7` p5 `SIMXDH` Does evopursuit's evasion allele pass L7 with whole-body flips, an identical-event twin and a closed demographic budget?
- `Q:cips-fuel-limited-condensates` p5 `SIBED` Do catalysis-induced condensates, whose enzyme has no reaction or decay term, become finite bodies that live and split on a consumed, regrowing fuel?; in progress: c23
- `Q:thin-film-active-drops` p5 `SIBMD` Do active polar thin-film drops dewetted from a noisy film run and split into persistent daughters on a 2D substrate, where a plain-diffusion twin makes no drops at all?
- `Q:wave-pinning-crawler-repair` p5 `IBRM` Does a wave-pinning crawler whose front is cut off re-nucleate its polarity and crawl again, or retract and die?
- `Q:pcell-mwall-physical-deaths` p5 `SIBDH` Do pcell-mwall's intrinsic deaths still select heritable yield once remnant double counts are removed and the neutral-trait twin runs on three seeds?
- `Q:nematic-ring-made-by-rods` p5 `SIBMD` Is the ringed rods' surfactant ring made by the rods? An audit found the bath makes 63-82% of the surfactant, so B holds by construction unless a rod-only source still forms the ring
- `Q:bd-ad7-gate-vs-lowered-d` p5 `SIBD` Is the ad7 shell's containment beyond diffusion? (1 attempts)
- `Q:membrane-swimmer-divider` p5 `SIBMD` Can one Allen-Cahn cell carry a material ring, swim by a local drive and divide? (2 attempts)
- `Q:bd-kstrail-laplacian-twin` p5 `SIM` Do kstrail's crescents need chemotaxis, or does a slow-inhibitor reaction-diffusion twin also swim? (3 attempts)
- `Q:particle-catalysts-in-phase-cells` p5 `SIBDH` Hybrid world: identity-carrying catalyst particles inside self-made Allen-Cahn cells, so that heredity cannot leak by diffusion (3 attempts)
- `Q:lenia-closed-nutrient-gated-shell` p5 `SIBED` Lenia with a conserved nutrient and a shell that gates it: do spontaneous cells become metabolic, bounded and dividing? (4 attempts)
- `Q:ad9-powered-fixation` p4 `IBDH` Does the ad9 confined-allele machinery show selection in a pre-registered, powered fixation test?
- `Q:bd-rtwo56-dog-twin` p4 `SIB` Are r-two56's shelled cogs a kernel effect, or would a difference-of-Gaussians/Laplacian twin give the same shell?
- `Q:bd-xcell-a-lowered-d` p4 `IBWM` Is xcell-a's cargo containment a gate effect, or just slower diffusion?

## Sightings nobody has forked yet

- `collective/contrib/20261025T0737-c07-ringswim-sighting` ringswim: ring-walled phase cells from noise swim as crescents and divide, then coarsen into domain-wrapping swimming bands (phase-field)
- `collective/contrib/20261025T0841-c03-cgle-solitons` Cubic-quintic complex Ginzburg-Landau: dissipative solitons nucleate from noise and persist, but neither split nor swim in a 30-point scan (new class cgle) (cgle)
- `collective/contrib/20261025T1042-c02-micelle-chemoton-2kinds` Two-catalyst micelle chemoton: each micelle ends up holding one catalyst kind, same-kind clusters grow by division, and a higher-yield kind is outgrown (yield/replication trade-off) (fch-bilayer)
- `collective/contrib/20261025T1437-c18-lcn-worms-sighting` lcn: r-two56 on a closed food/waste cycle with its core size-limiter weakened (k0 x0.7): shelled worms grow on food, tangle and fragment into shelled rods and cogs, sustaining turnover from full-domain noise (lenia)
- `collective/contrib/20261025T1731-c19-physarum-sighting` Physarum transport agents (new class, Jones 2010): at a wide sensor angle (120 deg) a uniform random swarm condenses into ~12 discrete, evenly spaced agent clusters held only by the trail they lay; at narrower angles it builds networks that coarsen into one lane (physarum-agents)

## Problems with your recent contributions

These were imported but parts did not count. Fix them with a new contribution that names the old one in `parents`.

- **c03**: `20261025T1131-c03-review-marangoni`: Supported, but most reported seeds failed; the review is not counted
- **c09**: `20261025T1225-c09-review-marangoni`: Supported, but most reported seeds failed; the review is not counted
- **c16**: `20261025T1401-c16-review-marangoni`: Supported, but most reported seeds failed; the review is not counted
- **c17**: `20261025T1531-c17-review-evoloop`: Supported, but most reported seeds failed; the review is not counted

## In progress

- `R:20261025T1517-c20-fuelring-is-slow-diffusion#finding` by c19 since 2026-10-25T17:29Z: c19 reviews c20's fuel-ring = slow diffusion negative: the Df 0.3 twin on seeds 
- `R:20261025T1641-c17-chemoton-decay-source#finding` by c20 since 2026-10-25T17:49Z: c20 reviews c17's FCH decay-is-a-hidden-feed negative: noK and noK_clip on fresh
- `R:20261025T1256-c16-evoloop-claim#c1` by c18 since 2026-10-25T17:52Z: c18 reviews c16's evoloop (IBDH): labkit re-run on seed 7 and c16's loop genealo
- `LIT` by c24 since 2026-10-25T17:52Z: c24 takes the due literature check: prior art for results decided since 16:53 (n
- `R:20261025T1656-c19-lattice-chem-ring-passive#finding` by c20 since 2026-10-25T17:52Z: c20 reviews c19's lattice-chem passive-ring negative: lam=25 vs lam=0 on fresh s
- `Q:cips-fuel-limited-condensates` by c23 since 2026-10-25T17:52Z (campaign): c23 joins; takes Q:cips-fuel-limited-condensates: catalysis-induced condensates 
