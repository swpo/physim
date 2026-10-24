# Evidence pack: evopursuit (seed 1)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 314s; status ok
- command: `WORLD_P='{"m":0,"B0":0,"k":0,"qdeath":0}' python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/arms_A_esc_s1 --seeds 1 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9674], min area 6 px

## Measurements
- components: final 19, mean 18.9, max 25; occupancy final 0.06
- tracks: 369; persistent (alive >= 50% of run): 0; longest 49 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 18, 16], H1 [0, 0, 0]
- motion: 24 long-lived tracks moved >= 1 body length; max speed 0.303/time; max body lengths 17.4
- replication (lineage window K = 20 frames = time 240, default): splits 85, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 91, merge/split ratio 1.07, nucleations 114
- channel total drift (end/start - 1): [0.4109, None, 0.0048, -0.0901]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 128 at frame 58: holes 0, rim-vs-core 0.42, rim-vs-outside 0.43, heterogeneity 0.12; core [0.977, 0.0, 0.453, 0.086] rim [0.855, 0.0, 0.081, 0.229]
  - track 124 at frame 53: holes 0, rim-vs-core 0.36, rim-vs-outside 0.43, heterogeneity 0.11; core [0.981, 0.0, 0.417, 0.101] rim [0.865, 0.0, 0.105, 0.243]
  - track 268 at frame 106: holes 0, rim-vs-core 0.24, rim-vs-outside 0.51, heterogeneity 0.12; core [0.977, 0.0, 0.42, 0.115] rim [0.893, 0.0, 0.211, 0.187]
  - track 291 at frame 110: holes 0, rim-vs-core 0.39, rim-vs-outside 0.43, heterogeneity 0.13; core [0.975, 0.0, 0.474, 0.113] rim [0.835, 0.0, 0.14, 0.26]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 119 components >= 12 px at frames [21, 42, 63, 83, 104, 125]):
  - radial preyA: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 14.5 (aggregate of 119 individuals; 2/119 membrane-like individually; rim level 0.842)
  - radial preyB: flat profile (no radial structure; level 0; aggregate of 119 individuals)
  - radial predator: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.504, rim/outside 20.5 (aggregate of 119 individuals; 1/119 membrane-like individually; rim level 0.296)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 6.29, rim/outside 0.674 (aggregate of 119 individuals; 0/119 membrane-like individually; rim level 0.51)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #128 (t=696, R_eq 4.26): none; #124 (t=636, R_eq 4.62): none; #268 (t=1272, R_eq 4.65): none; #291 (t=1320, R_eq 4.69): none
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 18, mean 18.7, max 26; tracks 422, persistent 0; splits 116, persistent splits 1 (K=20), max generation 1, merges 125, merge/split 1.08; moving tracks 19
- species `predator` (channels ['predator'], own threshold): components final 12, mean 13.4, max 23; tracks 237, persistent 0; splits 20, persistent splits 2 (K=20), max generation 1, merges 7, merge/split 0.35; moving tracks 21

## Warnings
- radial: 1 of 119 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
