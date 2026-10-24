# FINAL: chemotaxis-motility (3 sprints)

## Best worlds (committee consensus rungs, after the r1 and r2 reviews)
| world | consensus | what it shows | key packs |
|---|---|---|---|
| `kstrail` | **L4b[L2]** (high confidence); L3 Weak | Spontaneous self-propelled crescent swimmers from noise. A fast attractant holds the body, and a slow self-secreted repellent pushes it off its own wake. Formation route: spot → expanding ring → rupture → crescent. | `packs/kstrail`, `kstrail_abl_noh` (chi_h=0: static spots), `kstrail_dthalf` |
| `toxforage` | L4b[L2]; L4c Weak (near-Supported); L4a Weak | The trail is also toxic waste and growth needs a regrowing nutrient. A stationary population of swimmers with turnover: clumps poison themselves and re-shed swimmers. | `packs/toxforage`, `toxforage_abl_r0` |
| `swimfission` | **L6[L2]** + L4b (medium; reticulate: merges outnumber splits) | Fed swimmers divide by waist pinching once they outgrow the attractant's range (Da 4 → 2). Strict-rule depth: generation 3 in 3/3 seeds and at dt/2. | `packs/swimfission`, `fission_swimfission_s*` |
| `evopursuit` | **L5[L2]** + L4b (medium); L6 Weak; L7 Weak (near-Supported) (r2 consensus; r3 not yet reviewed) | Prey swimmers carry a heritable evasion allele. It sweeps in 3/3 seeds with predators, never with a neutral allele or without predators. Sprint 3: the allele exploits the chase (escorts help more than consuming predators) rather than escaping predation. | `packs/evopursuit*`, `packs/arms_*` |
| `pursuit`, `ecology` | L4b[L2], L5 Weak / low | Non-reciprocal cross-taxis binds chaser-fleer pairs. The ecology's "predation lowers prey" claim was withdrawn after the committee's matched control. | `packs/pursuit*`, `packs/ecology*` |

## Mechanisms that worked (with the ablation that shows it)
1. **Self-propulsion from a slow self-made repellent** (Keller-Segel + a second, slow trail chemical). chi_h = 0 gives static spots
   (`kstrail_abl_noh`). It works only in a window (chi_h ≈ 4-6.5 at chi_a 24) and **only for unsaturated bodies**: volume-filled plateaus
   have no gradient across them and stop. Precedents: Krischer & Mikhailov 1994 (RD travelling spots), Kranz et al. 2016 (trail particles).
2. **Toxic trail = size control + turnover.** If the trail also kills its maker (kd h rho), clumps poison themselves and re-shed swimmers.
   Mass-conserving swimmers coarsen into 2 immotile blobs by t=1800 (`kstrail_long`); toxforage keeps 6-14 swimmers indefinitely.
3. **Fission when growth outruns the cohesion range** (Da 4 → 2 for the attractant): front-fed swimmers elongate and pinch at the waist.
   The rate rises from 3 to 10-15 per 1200 t, but Da 4 is not a zero-fission control.
4. **Non-reciprocal cross-taxis binds chaser-fleer composites** (pursuit 2x2 ablation: without pursuit, contact falls to chance).
5. **Own-density cooperative growth purifies bodies**, so alleles confined in a body are inherited through fission (borrowed from active-droplets).
6. **Selection through behaviour, decomposed in sprint 3.** The evasion allele does not "escape predation". Being chased by
   non-consuming escorts more than doubles prey mass, and B gains more than A. Consumption then subtracts (A collapses, B survives).
   18 fixed-allele runs: prey mass ×2.4-2.5 (B + escort) > ×1.3 (B + predator) > ×0.4-0.5 (B alone), and A + predator collapses.
   Being chased raises prey speed (0.27 → 0.41 px/t for B with escorts). The benefit plausibly comes from leaving the self-toxic wake and
   reaching fresh food, but that causal step was not isolated. In the evolving runs, B births by clean fission exceed mutation conversions
   only 1.6x (46 vs 28, 3 seeds), so this is selection with real but partial fission heredity (L7 Weak).

## Mechanisms that failed
- Plain Keller-Segel with clipping (mass loss); explicit cubic pressure (NaN); nutrient chemotaxis alone (static lattice or extinction);
  Allee kinetics switched on before condensation (extinction); stronger growth alone (fragmentation, not fission); predator-prey
  kinetics never gave sustained cycles (stable coexistence only).
- labkit's sampling (6-12 t) cannot follow fission of moving bodies. My own trackers sample every 2 t (`fission.py`, `preytrack.py`).

## What transfers to PhySim worlds
- A **slow inhibitor/repellent secreted by the body** is a one-line operator that makes any aggregating field self-propelled. It needs bounded,
  unsaturated bodies. A conservative MUSCL volume-filling flux and resolved bodies (radius ≥ 6 px) avoid grid-locked headings.
- **Self-toxic waste** is a cheap homeostat: it caps body size, breaks up clumps and keeps a motile phase alive with turnover.
- **Non-reciprocal couplings between species** (one climbs, the other flees) create bound, moving composites. They are a natural source of
  L5 interactions and of selection on behaviour.
- Discovery-world angle: the hidden law in evopursuit is a sign flip. A partner that looks like a predator is a net benefactor through
  the chase, and an agent has to find that from the decomposition, not from the totals.

## What a next lab should try
- The Laplacian-only control (activator + slow inhibitor RD) for trail swimmers, to measure what advection adds.
- Coevolution (a heritable pursuit allele in predators) now that the chase/consumption decomposition is known.
- A gated-mobility membrane (autopoiesis, fisim) inside a swimmer: an L3 motile cell.
- Identical-event neutral twins with a shared mutation schedule (fisim) and per-event conversion accounting from the start.


## Showcase movie: `movies/showcase.mp4`
**evopursuit, seed 0, 192², t = 0-1500 (301 frames, 20 fps, fixed colours).** A uniform noisy soup of prey (cyan) and predator (magenta)
material condenses into self-propelled crescent swimmers within ~150 time units. Predators chase prey and ride in their concave rears. The
dark green wakes are food the prey have eaten; prey grow, poison themselves with their own trail, and divide by pinching. The ancestral A
prey are eaten down (32 bodies at t=200, 8 at t=750) while mutant prey carrying the B evasion allele (orange) appear by rare patch
mutations, divide true and spread, until at t≈1460 there are 45 B prey and no A. The strip at the bottom shows prey-A, prey-B and predator
mass. Watch for the reversal: once prey flee hard enough, the predator population grows *with* them. The decomposition in REPORT_r3 shows
that the chase itself is what B exploits.
