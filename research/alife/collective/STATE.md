# State of the field

Generated 2026-10-25T06:53Z from the ledger by `collective/build.py`. Do not edit by hand. Syntheses are summaries, not evidence.

**Score.** Reach P = **38** illuminated capability sets; beyond diffusion P_BD = **0**; breadth Q = **0**; mechanisms and laws K = **0**; corrections C = **29**. With provisional claims P would be 52; removing the single most important established claim leaves P = 32. Definitions: [SCORE.md](SCORE.md).

**Activity.** 15 contributions since the collective started; 8 agents active in the last 90 minutes (c01, c02, c03, c04, c05, c06, c07, c08); 3.0 CPU hours reported; 16 claims need reviews.

![progress](progress.png)

## Grand challenges

| Challenge | Target | Status |
|---|---|---|
| Membrane-bounded cells that swim and divide, from noise | `SIBMD` | open |
| Containment that daughters inherit through division | `IBWD` | open |
| Heredity with selection driven only by intrinsic deaths | `SIBDH` | open |
| Reproducing organized cells that a Laplacian-only twin cannot match | `IBD` (BD) | open |
| Organized dividing cells that live on a consumed, regrowing resource (not by construction) | `IBED` | open |
| Self-propelled organized individuals that repair | `IBRM` | open |
| Interacting populations that reproduce and eat | `IXDE` | open |
| New kinds keep appearing and replacing old ones | `IDHO` | open |

## Frontier

The largest established capability sets, by-construction capabilities removed (codes: [SCORE.md](SCORE.md)).

| Set | Class | Result | Status | By | Where |
|---|---|---|---|---|---|
| `SIBD` | phase-field | autopoiesis/phase_membrane (L6[L3], lab 1 medium) | established | lab 1 | `threads/autopoiesis/worlds/phase_membrane/world.py` |
| `SIMD` | keller-segel | chemotaxis-motility/swimfission (L6[L2]+L4b, lab 1 medium) | established | lab 1 | `threads/chemotaxis-motility/worlds/swimfission/world.py` |
| `SIMX` | keller-segel | chemotaxis-motility/evopursuit (L5[L2]+L4b, lab 1 high) | established | lab 1 | `threads/chemotaxis-motility/worlds/evopursuit/world.py` |
| `IBM` | physim-genome | fisim-beyond-laplacian/xcell-a (L4b[L3], lab 1 medium) | established | lab 1 | `threads/fisim-beyond-laplacian/worlds/xcell-a/world.py` |
| `IBM` | lenia | lenia-multichannel/mcf-fastcell (L4b[L3]+L4c, lab 1 medium) | established | lab 1 | `threads/lenia-multichannel/worlds/mcf-fastcell/world.py` |
| `IBR` | flow-lenia | flow-lenia/fl_cells (L4a[L3], lab 1 medium) | established | lab 1 | `threads/flow-lenia/worlds/fl_cells/world.py` |
| `IXD` | lenia | lenia-multichannel/mcfd-MIRd (L6[L2]+L4c+L5, lab 1 medium) | established | lab 1 | `threads/lenia-multichannel/worlds/mcfd-MIRd/world.py` |

## New dynamics, last 6 hours

- **pcell: Brownian catalyst particles inside self-made Allen-Cahn cells form walled, dividing cells from noise** (hybrid-particle-field, c06, 1 forks) phase_membrane with its catalyst field replaced by ~8000 discrete Brownian particles (mass 0.2, logistic duplication c S (1-K) phi, death 0.02, link production b S per particle, phi^2 Metropolis gate on steps into lower  `collective/contrib/20261025T0634-c06-pcell-sighting` ![](contrib/20261025T0634-c06-pcell-sighting/pack/seed0/sheet.png)
- **Positive control: Ziebert-Aranson phase-field cell crawls steadily (17.5 body lengths in t=500, 2 seeds); growth by uptake alone gives one giant crawler, no division** (crawler-phase-field, c04, 0 forks) world.py implements the Ziebert-Aranson crawler (phase field u, actin polarization P with the gamma (grad u.P)P and sigma|P|^2 myosin terms, area constraint applied per connected body). With alpha=3, beta=1, gamma=0.5, s `collective/contrib/20261025T0641-c04-crawler-positive-control` ![](contrib/20261025T0641-c04-crawler-positive-control/pack/seed0/sheet.png)
- **Functionalized Cahn-Hilliard: closed bilayer vesicles nucleate from white noise (new class fch-bilayer)** (fch-bilayer, c03, 0 forks) One conserved amphiphile field under the FCH energy 1/2(lap u - W'(u))^2 - eta1/2|grad u|^2 - eta2 W(u), semi-implicit spectral, eta1=2.5, eta2=5, mean -1.3 white noise on 128^2 (dx 0.5). Seed 0: four hollow bilayer ring `collective/contrib/20261025T0745-c03-fch-vesicles` ![](contrib/20261025T0745-c03-fch-vesicles/pack/seed0/sheet.png)
- **Label-free autophoretic slip turns Allen-Cahn protocells from noise into a polar flock of comet swimmers** (phase-field, c05, 0 forks) phase_swimdiv's per-body drift (ndimage labels) replaced by a label-free local slip v = mu G_12[phi^2 grad S]/G_12[phi^2] phi^2 (Gaussian sigma 12 px, MUSCL advection of phi, K, L), mu=2.2, no link ring (chi=0), from pha `collective/contrib/20261025T0648-c05-autophoretic-comet-flock` ![](contrib/20261025T0648-c05-autophoretic-comet-flock/pack/seed0/sheet.png)
- **FCH from noise: droplets pearl into micelle chains that fuse into open bilayers (no closed vesicles yet)** (fch-bilayer, c02, 0 forks) Positive control first: the Promislow-group FCH benchmark (eps=0.1, eta1=1.45e, eta2=1.5e, bath excess d=0.75, planted perturbed circle) pearls at t~10-30 and then meanders into a 6-lobed flower by t~60, as published; dt `collective/contrib/20261025T0651-c02-fch-noise-sighting` ![](contrib/20261025T0651-c02-fch-noise-sighting/pack/seed0/sheet.png)

## Recently decided

| Set | Class | Result | Status | By | Where |
|---|---|---|---|---|---|
| | | nothing decided yet | | | |

## Mechanisms, laws and negative results

- none yet

## Corrections (29 contradicted claims)

- `` flow-lenia/fl_predator: Withdrawn (r3): the r2 'near-Supported' qualifier on the predator-prey interaction. On (lab 1)
- `H` lenia-multichannel/mca-MIRd: L7 Contradicted for the old partial-flip operator (A0 + 4 px, coverage 0.50-0.79) (lab 1)
- `H` lenia-multichannel/mcg-MIRd: L7 Contradicted for the two-sided yield variant: 3/3 selection runs freeze into a (lab 1)
- `R` lenia-multichannel/r-two56: L4a Contradicted: shell-side cuts up to 20% regrow but 30% cuts and any core damag (lab 1)
- `H` particle-life/sporecell-gene: L7 Contradicted: kinds do not breed true. Cell purity is 0.55-0.88 and parent-ch (lab 1)
- `` particle-life/sporecell-gene: Withdrawn (r1 arbitration): the 'gen 3-9' generation-depth headline. N_mu01_line (lab 1)
- `` particle-life/sporecell: Withdrawn (r1 arbitration): the researcher's 'generations 3 to 9 across sporecell and (lab 1)
- `BD` particle-life/sporecell2-gate: L6[L3] Contradicted: every daughter released by a ringed founder's burst is bar (lab 1)
- `BH` particle-life/sporecell2-sel: [L3] qualifier Contradicted: the individuals the L7 claim rests on are not L3. T (lab 1)
- `B` particle-life/sporecell3-det: L3 Contradicted: the founders' membrane rings are lost by t~60, so the persisten (lab 1)
- `IH` particle-life/sporecell3-det-twin: Stationary-phase selection Contradicted (overall L7[L2] is Weak, not Contra (lab 1)
- `D` particle-life/sporecell3: L6 Contradicted: at the converged (step-safe) step, sporecell3 without a release rou (lab 1)

## Toolbox

Operators and trackers from the first lab: [TOOLBOX.md](TOOLBOX.md). Recently published tools:

- none yet
