# Evidence pack: evopursuit (seed 2)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 307s; status ok
- command: `WORLD_P='{"m":0,"B0":1,"pred":0}' python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/arms_B_none_s2 --seeds 2 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9944], min area 6 px

## Measurements
- components: final 11, mean 14.0, max 28; occupancy final 0.03
- tracks: 155; persistent (alive >= 50% of run): 1; longest 71 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 19.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 11], H1 [0, 0, 0]
- motion: 32 long-lived tracks moved >= 1 body length; max speed 0.286/time; max body lengths 24.0
- replication (lineage window K = 20 frames = time 240, default): splits 35, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 50, merge/split ratio 1.43, nucleations 43
- channel total drift (end/start - 1): [None, -0.4567, None, -0.0338]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 39: holes 0, rim-vs-core 0.59, rim-vs-outside 0.49, heterogeneity 0.15; core [0.598, 0.949, 0.0, 0.116] rim [0.319, 0.506, 0.0, 0.378]
  - track 56 at frame 49: holes 0, rim-vs-core 0.65, rim-vs-outside 0.62, heterogeneity 0.17; core [0.995, 0.943, 0.0, 0.123] rim [0.624, 0.475, 0.0, 0.385]
  - track 37 at frame 39: holes 0, rim-vs-core 0.45, rim-vs-outside 0.52, heterogeneity 0.13; core [0.252, 0.977, 0.0, 0.07] rim [0.172, 0.601, 0.0, 0.302]
  - track 75 at frame 58: holes 0, rim-vs-core 0.57, rim-vs-outside 0.69, heterogeneity 0.15; core [1.0, 0.951, 0.0, 0.113] rim [0.719, 0.529, 0.0, 0.369]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 81 components >= 12 px at frames [21, 42, 63, 83, 104, 125]):
  - radial preyA: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.866, rim/outside 22 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.423)
  - radial preyB: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.81, rim/outside 37.7 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.796)
  - radial predator: flat profile (no radial structure; level 0; aggregate of 81 individuals)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 11.2, rim/outside 0.744 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.615)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=468, R_eq 5.08): none; #56 (t=588, R_eq 5.14): none; #37 (t=468, R_eq 5.47): none; #75 (t=696, R_eq 5.05): none
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 11, mean 14.0, max 28; tracks 155, persistent 1; splits 35, persistent splits 0 (K=20), max generation 0, merges 50, merge/split 1.43; moving tracks 32
- species `predator` (channels ['predator'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
