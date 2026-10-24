# Evidence pack: evopursuit (seed 2)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 305s; status ok
- command: `WORLD_P='{"m":0,"B0":1,"k":0,"qdeath":0}' python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/arms_B_esc_s2 --seeds 2 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9093], min area 6 px

## Measurements
- components: final 32, mean 32.1, max 43; occupancy final 0.10
- tracks: 1115; persistent (alive >= 50% of run): 0; longest 30 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 34, 28], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.284/time; max body lengths 12.5
- replication (lineage window K = 20 frames = time 240, default): splits 201, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 211, merge/split ratio 1.05, nucleations 540
- channel total drift (end/start - 1): [None, 1.4325, -0.0003, -0.1455]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 132 at frame 32: holes 0, rim-vs-core 0.17, rim-vs-outside 0.35, heterogeneity 0.06; core [0.027, 0.987, 0.101, 0.122] rim [0.027, 0.912, 0.012, 0.248]
  - track 199 at frame 39: holes 0, rim-vs-core 0.38, rim-vs-outside 0.40, heterogeneity 0.13; core [0.0, 0.936, 0.488, 0.222] rim [0.0, 0.802, 0.157, 0.344]
  - track 193 at frame 36: holes 0, rim-vs-core 0.31, rim-vs-outside 0.41, heterogeneity 0.13; core [0.217, 0.964, 0.342, 0.175] rim [0.175, 0.854, 0.083, 0.307]
  - track 200 at frame 37: holes 0, rim-vs-core 0.46, rim-vs-outside 0.37, heterogeneity 0.15; core [0.02, 0.943, 0.579, 0.106] rim [0.02, 0.824, 0.16, 0.26]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 189 components >= 12 px at frames [21, 42, 63, 83, 104, 125]):
  - radial preyA: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.943, rim/outside 6.28 (aggregate of 189 individuals; 8/189 membrane-like individually; rim level 0.199)
  - radial preyB: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 9.77 (aggregate of 189 individuals; 7/189 membrane-like individually; rim level 0.787)
  - radial predator: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.46, rim/outside 14.7 (aggregate of 189 individuals; 8/189 membrane-like individually; rim level 0.236)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.63, rim/outside 0.714 (aggregate of 189 individuals; 0/189 membrane-like individually; rim level 0.527)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #132 (t=384, R_eq 4.07): none; #199 (t=468, R_eq 4.79): none; #193 (t=432, R_eq 4.85): none; #200 (t=444, R_eq 4.82): none
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 32, mean 31.5, max 42; tracks 1403, persistent 0; splits 356, persistent splits 0 (K=20), max generation 0, merges 357, merge/split 1; moving tracks 4
- species `predator` (channels ['predator'], own threshold): components final 20, mean 19.5, max 27; tracks 979, persistent 0; splits 9, persistent splits 0 (K=20), max generation 0, merges 8, merge/split 0.889; moving tracks 3

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 189 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
