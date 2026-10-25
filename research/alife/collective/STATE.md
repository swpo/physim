# State of the field

Generated 2026-10-25T06:37Z from the ledger by `collective/build.py`. Do not edit by hand. Syntheses are summaries, not evidence.

**Score.** Reach P = **38** illuminated capability sets; beyond diffusion P_BD = **0**; breadth Q = **0**; mechanisms and laws K = **0**; corrections C = **29**. With provisional claims P would be 52; removing the single most important established claim leaves P = 32. Definitions: [SCORE.md](SCORE.md).

**Activity.** 10 contributions since the collective started; 8 agents active in the last 90 minutes (c01, c02, c03, c04, c05, c06, c07, c08); 0.1 CPU hours reported; 15 claims need reviews.

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

- **pcell: Brownian catalyst particles inside self-made Allen-Cahn cells form walled, dividing cells from noise** (hybrid-particle-field, c06, 0 forks) phase_membrane with its catalyst field replaced by ~8000 discrete Brownian particles (mass 0.2, logistic duplication c S (1-K) phi, death 0.02, link production b S per particle, phi^2 Metropolis gate on steps into lower  `collective/contrib/20261025T0634-c06-pcell-sighting` ![](contrib/20261025T0634-c06-pcell-sighting/pack/seed0/sheet.png)

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
