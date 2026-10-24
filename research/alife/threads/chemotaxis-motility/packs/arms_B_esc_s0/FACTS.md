# Evidence pack: evopursuit (seed 0)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 303s; status ok
- command: `WORLD_P='{"m":0,"B0":1,"k":0,"qdeath":0}' python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/arms_B_esc_s0 --seeds 0 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9078], min area 6 px

## Measurements
- components: final 35, mean 30.2, max 39; occupancy final 0.10
- tracks: 1057; persistent (alive >= 50% of run): 0; longest 34 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 38, 30], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.274/time; max body lengths 10.2
- replication (lineage window K = 20 frames = time 240, default): splits 206, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 174, merge/split ratio 0.845, nucleations 495
- channel total drift (end/start - 1): [None, 1.4318, 0.0, -0.1457]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 378 at frame 61: holes 0, rim-vs-core 0.34, rim-vs-outside 0.65, heterogeneity 0.12; core [0.444, 0.976, 0.474, 0.005] rim [0.378, 0.858, 0.178, 0.094]
  - track 505 at frame 71: holes 0, rim-vs-core 0.18, rim-vs-outside 0.35, heterogeneity 0.07; core [0.056, 0.982, 0.138, 0.032] rim [0.057, 0.915, 0.017, 0.141]
  - track 351 at frame 51: holes 0, rim-vs-core 0.37, rim-vs-outside 0.43, heterogeneity 0.19; core [0.472, 0.983, 0.408, 0.079] rim [0.491, 0.891, 0.074, 0.219]
  - track 413 at frame 60: holes 0, rim-vs-core 0.14, rim-vs-outside 0.30, heterogeneity 0.05; core [0.0, 0.99, 0.044, 0.121] rim [0.0, 0.935, 0.007, 0.243]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 181 components >= 12 px at frames [21, 42, 63, 83, 104, 125]):
  - radial preyA: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.929, rim/outside 7.04 (aggregate of 181 individuals; 9/181 membrane-like individually; rim level 0.243)
  - radial preyB: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.886, rim/outside 10.7 (aggregate of 181 individuals; 5/181 membrane-like individually; rim level 0.808)
  - radial predator: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.443, rim/outside 16.2 (aggregate of 181 individuals; 5/181 membrane-like individually; rim level 0.239)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.04, rim/outside 0.701 (aggregate of 181 individuals; 0/181 membrane-like individually; rim level 0.518)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #378 (t=732, R_eq 6.18): none; #505 (t=852, R_eq 5.73): none; #351 (t=612, R_eq 5.14): none; #413 (t=720, R_eq 3.83): none
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 34, mean 29.9, max 40; tracks 1334, persistent 0; splits 340, persistent splits 0 (K=20), max generation 0, merges 337, merge/split 0.991; moving tracks 2
- species `predator` (channels ['predator'], own threshold): components final 22, mean 19.6, max 27; tracks 967, persistent 0; splits 10, persistent splits 0 (K=20), max generation 0, merges 13, merge/split 1.3; moving tracks 2

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 181 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
