# Evidence pack: evopursuit (seed 1)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 311s; status ok
- command: `WORLD_P='{"m":0,"B0":1}' python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/arms_B_pred_s1 --seeds 1 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9043], min area 6 px

## Measurements
- components: final 30, mean 29.8, max 40; occupancy final 0.06
- tracks: 1793; persistent (alive >= 50% of run): 0; longest 19 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [39, 33, 27], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 8.6
- replication (lineage window K = 20 frames = time 240, default): splits 39, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 46, merge/split ratio 1.18, nucleations 1668
- channel total drift (end/start - 1): [None, 0.3216, 0.8105, -0.0906]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 359 at frame 36: holes 0, rim-vs-core 0.36, rim-vs-outside 0.46, heterogeneity 0.23; core [0.269, 0.961, 0.538, 0.023] rim [0.185, 0.64, 0.485, 0.138]
  - track 86 at frame 19: holes 0, rim-vs-core 0.32, rim-vs-outside 0.29, heterogeneity 0.23; core [0.0, 0.551, 0.687, 0.232] rim [0.0, 0.516, 0.4, 0.363]
  - track 1099 at frame 82: holes 0, rim-vs-core 0.55, rim-vs-outside 0.50, heterogeneity 0.31; core [0.112, 0.205, 0.861, 0.105] rim [0.31, 0.495, 0.453, 0.226]
  - track 733 at frame 57: holes 0, rim-vs-core 0.47, rim-vs-outside 0.44, heterogeneity 0.26; core [0.354, 0.891, 0.657, 0.062] rim [0.32, 0.61, 0.332, 0.245]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 186 components >= 12 px at frames [21, 42, 63, 83, 104, 125]):
  - radial preyA: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.855, rim/outside 4.62 (aggregate of 186 individuals; 17/186 membrane-like individually; rim level 0.229)
  - radial preyB: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.825, rim/outside 6.76 (aggregate of 186 individuals; 22/186 membrane-like individually; rim level 0.591)
  - radial predator: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.586, rim/outside 9.34 (aggregate of 186 individuals; 4/186 membrane-like individually; rim level 0.425)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.38, rim/outside 0.751 (aggregate of 186 individuals; 0/186 membrane-like individually; rim level 0.543)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #359 (t=432, R_eq 4.26): none; #86 (t=228, R_eq 4.65): none; #1099 (t=984, R_eq 7.31): ['preyA', 'preyB']; #733 (t=684, R_eq 4.48): none
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 37, mean 31.8, max 41; tracks 1577, persistent 0; splits 42, persistent splits 0 (K=20), max generation 0, merges 54, merge/split 1.29; moving tracks 0
- species `predator` (channels ['predator'], own threshold): components final 27, mean 23.6, max 32; tracks 1774, persistent 0; splits 5, persistent splits 0 (K=20), max generation 0, merges 17, merge/split 3.4; moving tracks 4

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 186 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
