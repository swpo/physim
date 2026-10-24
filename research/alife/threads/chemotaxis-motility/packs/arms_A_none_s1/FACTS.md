# Evidence pack: evopursuit (seed 1)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 304s; status ok
- command: `WORLD_P='{"m":0,"B0":0,"pred":0}' python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/arms_A_none_s1 --seeds 1 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9963], min area 6 px

## Measurements
- components: final 8, mean 14.3, max 28; occupancy final 0.03
- tracks: 208; persistent (alive >= 50% of run): 1; longest 67 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.90 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [0, 0, 0]
- motion: 21 long-lived tracks moved >= 1 body length; max speed 0.279/time; max body lengths 19.5
- replication (lineage window K = 20 frames = time 240, default): splits 47, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 67, merge/split ratio 1.43, nucleations 50
- channel total drift (end/start - 1): [-0.4392, None, None, -0.0363]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 145 at frame 92: holes 0, rim-vs-core 0.49, rim-vs-outside 0.46, heterogeneity 0.10; core [0.957, 0.0, 0.0, 0.111] rim [0.548, 0.0, 0.0, 0.372]
  - track 159 at frame 97: holes 0, rim-vs-core 0.47, rim-vs-outside 0.46, heterogeneity 0.10; core [0.958, 0.0, 0.0, 0.109] rim [0.557, 0.0, 0.0, 0.361]
  - track 167 at frame 100: holes 0, rim-vs-core 0.48, rim-vs-outside 0.46, heterogeneity 0.10; core [0.959, 0.0, 0.0, 0.108] rim [0.551, 0.0, 0.0, 0.355]
  - track 189 at frame 106: holes 0, rim-vs-core 0.50, rim-vs-outside 0.43, heterogeneity 0.11; core [0.946, 0.0, 0.0, 0.148] rim [0.522, 0.0, 0.0, 0.407]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 82 components >= 12 px at frames [21, 42, 63, 83, 104, 125]):
  - radial preyA: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.803, rim/outside 38.1 (aggregate of 82 individuals; 1/82 membrane-like individually; rim level 0.775)
  - radial preyB: flat profile (no radial structure; level 0; aggregate of 82 individuals)
  - radial predator: flat profile (no radial structure; level 0; aggregate of 82 individuals)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 11.9, rim/outside 0.748 (aggregate of 82 individuals; 0/82 membrane-like individually; rim level 0.636)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #145 (t=1104, R_eq 5.26): none; #159 (t=1164, R_eq 5.23): none; #167 (t=1200, R_eq 5.23): none; #189 (t=1272, R_eq 4.72): none
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 8, mean 14.3, max 28; tracks 208, persistent 1; splits 47, persistent splits 1 (K=20), max generation 1, merges 67, merge/split 1.43; moving tracks 21
- species `predator` (channels ['predator'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- radial: 1 of 82 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
