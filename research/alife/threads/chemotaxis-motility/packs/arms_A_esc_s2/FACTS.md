# Evidence pack: evopursuit (seed 2)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 308s; status ok
- command: `WORLD_P='{"m":0,"B0":0,"k":0,"qdeath":0}' python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/arms_A_esc_s2 --seeds 2 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9544], min area 6 px

## Measurements
- components: final 17, mean 18.6, max 25; occupancy final 0.06
- tracks: 353; persistent (alive >= 50% of run): 0; longest 56 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 14], H1 [0, 0, 0]
- motion: 23 long-lived tracks moved >= 1 body length; max speed 0.304/time; max body lengths 20.0
- replication (lineage window K = 20 frames = time 240, default): splits 83, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 93, merge/split ratio 1.12, nucleations 104
- channel total drift (end/start - 1): [0.2241, None, 0.0544, -0.0796]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 137 at frame 66: holes 0, rim-vs-core 0.34, rim-vs-outside 0.36, heterogeneity 0.15; core [0.935, 0.0, 0.436, 0.167] rim [0.713, 0.0, 0.235, 0.327]
  - track 131 at frame 61: holes 0, rim-vs-core 0.38, rim-vs-outside 0.55, heterogeneity 0.17; core [0.925, 0.0, 0.686, 0.227] rim [0.735, 0.0, 0.376, 0.336]
  - track 140 at frame 61: holes 0, rim-vs-core 0.30, rim-vs-outside 0.40, heterogeneity 0.10; core [0.983, 0.0, 0.323, 0.096] rim [0.873, 0.0, 0.083, 0.244]
  - track 160 at frame 71: holes 0, rim-vs-core 0.13, rim-vs-outside 0.30, heterogeneity 0.05; core [0.977, 0.0, 0.118, 0.237] rim [0.905, 0.0, 0.055, 0.319]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 109 components >= 12 px at frames [21, 42, 63, 83, 104, 125]):
  - radial preyA: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 15.6 (aggregate of 109 individuals; 4/109 membrane-like individually; rim level 0.826)
  - radial preyB: flat profile (no radial structure; level 0; aggregate of 109 individuals)
  - radial predator: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.489, rim/outside 21.5 (aggregate of 109 individuals; 0/109 membrane-like individually; rim level 0.292)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 6.65, rim/outside 0.673 (aggregate of 109 individuals; 0/109 membrane-like individually; rim level 0.519)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #137 (t=792, R_eq 5.17): none; #131 (t=732, R_eq 4.11): none; #140 (t=732, R_eq 4.55): none; #160 (t=852, R_eq 2.52): none
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 17, mean 18.4, max 24; tracks 397, persistent 0; splits 108, persistent splits 1 (K=20), max generation 1, merges 125, merge/split 1.16; moving tracks 19
- species `predator` (channels ['predator'], own threshold): components final 11, mean 12.2, max 20; tracks 242, persistent 0; splits 17, persistent splits 0 (K=20), max generation 0, merges 8, merge/split 0.471; moving tracks 18

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
