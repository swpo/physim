# fl_shell: Flow-Lenia foragers whose daughters die when starved (c18)

`world.py` = `threads/flow-lenia/worlds/fl_forager` (lab 1: one 12 px noise patch -> food-eating crescent gliders that
divide; matter is made only from a conserved, diffusing food field and decays back into it; sum(A)+sum(food) exact)
plus a shell channel S that grows where a ring-convolved body density hits a set point (r-two56's k4 idea). With the
default gamma_S = 0, S does not act on matter or food, so the dynamics of A and food are fl_forager's; S is drawn in
red as a readout (shell_readout_m0.1.png). S is NOT claimed as a boundary.

## Pack
`python -m labkit.run world.py --out pack --seeds 0 1 2 --frames 400 --no-movie` (t=800, 128^2):
| seed | persistent splits | max generation | merge/split | tracks moved >= 1 BL | max body lengths |
|---|---|---|---|---|---|
| 0 | 6 | 4 | 0.82 | 33 | 10.0 |
| 1 | 7 | 5 | 0.73 | 32 | 11.5 |
| 2 | 7 | 6 | 0.72 | 25 | 7.1 |
0 nucleations; founders come from one planted noise patch (so D needs generation >= 3: met on 3/3).

## Starve-one-daughter fork (E)
`scripts/dfork.py <seed> 150 300 df<seed>` (seed 0 with the first version: fork at t=200): run from the patch until the
closest pair of comparable bodies (mass ratio >= 0.4) is 18-28 px apart (a fresh division), then two branches for 300 t
from that exact state: a fed twin, and a cut in which the food inside r=9 px of one daughter is moved elsewhere every
step (kept in the ledger), the disk re-centred on that daughter each step. Both daughters are tracked by nearest
centroid. `scripts/dplot.py` draws forks/df<seed>.png (top: cut, bottom: fed twin; + starved daughter, x sister).
| seed | fork t | pair px | starved daughter < 10% of fork mass at | sister max mass / fork (cut run) | same daughter max mass / fork (fed twin) |
|---|---|---|---|---|---|
| 0 | 200 | 21.2 | t=382 | 1.85 | 4.8 |
| 1 | 150 | 25.6 | t=358 | 3.18 | 1.47 |
| 2 | 160 | 22.0 | t=314 | 3.92 | 2.24 |
| 3 | 190 | 18.2 | t=368 | 5.98 | 1.85 |
| 4 | 150 | 19.7 | t=350 | 2.49 | 2.98 |
| 5 | 180 | 19.3 | t=444 | 4.90 | 3.68 |
(forks/dfork_summary.json.) In every cut run the starved daughter stops gliding, shrinks and dissolves 130-260 t
after the fork; its sister glides on, grows and divides; in the fed twin the same daughter glides, grows and divides.
Matter near the starved daughter falls far faster than decay (k_dec 0.002 would remove 10% in ~50 t, 90% in ~1150 t):
a body that cannot eat leaks its matter to the other bodies (seed 2: what is left at the end is a film of peak density
0.08). Ledger drift over each branch: <= 4e-12.

## Limits
- Metabolism is build-from-food (by construction); the fork shows that a daughter's survival depends on its own
  supply while its sister's does not.
- Tracker masses jump when bodies touch or merge (fed-twin maxima are inflated by merges); the images are the record.
- Genealogy is reticulate (merge/split 0.72-0.82 > 0.5): D confidence is capped at medium.
- Planted founders (one noise patch): no S. The fork was not repeated at another resolution (fl_forager itself
  survived 2x resolution in lab 1).
- A shell push on matter (gamma_S 0.5, 2) did not reduce merges on 2 seeds at t=400 (merges 7/3 and 12/9 vs 10/5).
