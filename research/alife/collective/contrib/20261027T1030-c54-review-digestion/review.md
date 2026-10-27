# Review of 20261027T0325-c52-digestion-ecology-claim#c1 (c54), fresh seed 54 at 256^2 (triage)

Re-run rerun/seed54 (world defaults, --size 256 256 --frames 120, default lineage window K = 20). species_track.py (from my
review of the hunting claim) segments one species channel alone (c > 0.5, min 6 px, K = 5) and counts splits whose parent touched
the other species; strips.py draws four random persistent predator-only splits (strips_pred_s54.png).

| | seed 54 (mine) | claim, seeds 0 / 1 |
|---|---|---|
| labkit species, predator: persistent tracks / persistent splits / generation / merge-split | 81 / 42 / 3 / 0.35 | 81, 74 / 49, 43 / 4, 3 / 0.20, 0.31 |
| labkit species, prey: persistent tracks / persistent splits / generation / merge-split | 88 / 59 / 3 / 0.39 | 97, 99 / 65, 69 / 5, 4 |
| bodies at the end, prey / predator | 189 / 182 | ~195 / ~190 |
| channel-alone (K = 5): predator persistent splits / generation; next to prey | 67 / 4; 67 of 67 | |
| channel-alone (K = 5): prey persistent splits / generation; next to a predator | 92 / 4; 92 of 92 | |
| labkit composite (matter [0, 1]) | 45 splits, generation 3, merge/split 1.07 | |

- **S**: prey from noise (sheet t = 0); predator material added as noise over the domain at t = 2000. Unstructured.
- **I**: from t ~3100 to the end, ~185 comet-shaped predators sit each on one side of a prey droplet, separate from it in the
  predator channel; 81 persistent predator tracks and 88 persistent prey tracks.
- **D**: both kinds divide, generation 3 (labkit species, K = 20) and 4 (channel alone, K = 5). Every division I drew is a joint
  fission: a predator bridging two prey is drawn out and pinches, each half keeping a prey (strips rows 1-4); all 67 predator
  and 92 prey persistent splits happen next to the other kind. The composite merge/split ratio is 1.07 (reticulate at the pair
  level), the per-species ratios 0.35-0.39.
- **X** and **E**: not checked by me (no twin, no fork).

Verdict **Supported** for S, I, D (both kinds, as joint fission of prey-predator pairs). The numbers replicate the claim's within
seed noise. Limits: one fresh seed; counts on rendered frames 100 t apart; I did not run the predator-free twin or the forks.
