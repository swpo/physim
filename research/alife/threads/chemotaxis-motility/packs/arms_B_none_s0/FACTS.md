# Evidence pack: evopursuit (seed 0)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 300s; status ok
- command: `WORLD_P='{"m":0,"B0":1,"pred":0}' python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/arms_B_none_s0 --seeds 0 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9936], min area 6 px

## Measurements
- components: final 6, mean 10.3, max 27; occupancy final 0.02
- tracks: 126; persistent (alive >= 50% of run): 1; longest 76 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.95 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 6], H1 [0, 0, 0]
- motion: 18 long-lived tracks moved >= 1 body length; max speed 0.265/time; max body lengths 25.2
- replication (lineage window K = 20 frames = time 240, default): splits 23, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 41, merge/split ratio 1.78, nucleations 41
- channel total drift (end/start - 1): [None, -0.6389, None, -0.022]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 86 at frame 88: holes 0, rim-vs-core 0.54, rim-vs-outside 0.45, heterogeneity 0.13; core [0.292, 0.949, 0.0, 0.09] rim [0.158, 0.493, 0.0, 0.345]
  - track 106 at frame 97: holes 0, rim-vs-core 0.52, rim-vs-outside 0.45, heterogeneity 0.12; core [0.223, 0.95, 0.0, 0.089] rim [0.121, 0.509, 0.0, 0.345]
  - track 43 at frame 41: holes 0, rim-vs-core 0.47, rim-vs-outside 0.45, heterogeneity 0.11; core [0.0, 0.957, 0.0, 0.081] rim [0.0, 0.547, 0.0, 0.319]
  - track 47 at frame 40: holes 0, rim-vs-core 0.50, rim-vs-outside 0.40, heterogeneity 0.11; core [0.0, 0.928, 0.0, 0.16] rim [0.0, 0.5, 0.0, 0.416]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 56 components >= 12 px at frames [21, 42, 63, 83, 104, 125]):
  - radial preyA: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.905, rim/outside 18.5 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.345)
  - radial preyB: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.807, rim/outside 35.1 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.792)
  - radial predator: flat profile (no radial structure; level 0; aggregate of 56 individuals)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 15.9, rim/outside 0.724 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.609)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #86 (t=1056, R_eq 5.08): none; #106 (t=1164, R_eq 5.08): none; #43 (t=492, R_eq 5.01): none; #47 (t=480, R_eq 4.22): none
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 6, mean 10.3, max 27; tracks 126, persistent 1; splits 23, persistent splits 0 (K=20), max generation 0, merges 41, merge/split 1.78; moving tracks 18
- species `predator` (channels ['predator'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
