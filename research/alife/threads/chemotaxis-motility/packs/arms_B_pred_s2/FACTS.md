# Evidence pack: evopursuit (seed 2)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 311s; status ok
- command: `WORLD_P='{"m":0,"B0":1}' python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/arms_B_pred_s2 --seeds 2 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9018], min area 6 px

## Measurements
- components: final 29, mean 30.1, max 42; occupancy final 0.07
- tracks: 1769; persistent (alive >= 50% of run): 0; longest 16 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 29, 20], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 7.7
- replication (lineage window K = 20 frames = time 240, default): splits 43, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 63, merge/split ratio 1.47, nucleations 1625
- channel total drift (end/start - 1): [None, 0.2845, 0.8806, -0.0917]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1137 at frame 88: holes 0, rim-vs-core 0.23, rim-vs-outside 0.31, heterogeneity 0.23; core [0.067, 0.572, 0.596, 0.281] rim [0.069, 0.568, 0.387, 0.366]
  - track 493 at frame 45: holes 0, rim-vs-core 0.32, rim-vs-outside 0.28, heterogeneity 0.28; core [0.116, 0.564, 0.683, 0.122] rim [0.088, 0.453, 0.451, 0.313]
  - track 710 at frame 61: holes 0, rim-vs-core 0.34, rim-vs-outside 0.39, heterogeneity 0.10; core [0.071, 0.967, 0.382, 0.024] rim [0.062, 0.829, 0.095, 0.152]
  - track 238 at frame 27: holes 0, rim-vs-core 0.35, rim-vs-outside 0.29, heterogeneity 0.26; core [0.096, 0.634, 0.629, 0.065] rim [0.095, 0.588, 0.324, 0.237]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 181 components >= 12 px at frames [21, 42, 63, 83, 104, 125]):
  - radial preyA: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.861, rim/outside 4.64 (aggregate of 181 individuals; 27/181 membrane-like individually; rim level 0.188)
  - radial preyB: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.85, rim/outside 6.8 (aggregate of 181 individuals; 31/181 membrane-like individually; rim level 0.58)
  - radial predator: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.579, rim/outside 10.5 (aggregate of 181 individuals; 3/181 membrane-like individually; rim level 0.43)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.31, rim/outside 0.746 (aggregate of 181 individuals; 0/181 membrane-like individually; rim level 0.538)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1137 (t=1056, R_eq 5.44): ['preyA', 'preyB']; #493 (t=540, R_eq 4.75): none; #710 (t=732, R_eq 3.7): none; #238 (t=324, R_eq 5.64): none
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 30, mean 32.1, max 45; tracks 1530, persistent 0; splits 60, persistent splits 0 (K=20), max generation 0, merges 57, merge/split 0.95; moving tracks 1
- species `predator` (channels ['predator'], own threshold): components final 23, mean 23.8, max 34; tracks 1788, persistent 0; splits 10, persistent splits 0 (K=20), max generation 0, merges 16, merge/split 1.6; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 181 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
