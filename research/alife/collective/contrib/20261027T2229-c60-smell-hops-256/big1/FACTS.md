# Evidence pack: digestion-predators-smell (seed 72)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261027T2152-c60-smell-predators/world.py`, family `active-emulsion`
- parent: collective/contrib/20261027T0325-c52-digestion-ecology-claim; mutation: predator fuel-depletion drift chiF 0.5 -> 0.25; before (c52): predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 2123s; status ok
- command: `python -m labkit.run collective/contrib/20261027T2152-c60-smell-predators/world.py --out /tmp/claude-0/smell/big1 --seeds 72 --size 256 256 --frames 120 --no-movie`
- segmentation: matter > 0.22 of robust range [0.1572, 1.6913], min area 6 px

## Measurements
- components: final 199, mean 176.6, max 209; occupancy final 0.18
- tracks: 1001; persistent (alive >= 50% of run): 67; longest 118 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 21.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [202, 186, 156], H1 [0, 0, 0]
- motion: 328 long-lived tracks moved >= 1 body length; max speed 0.00932/time; max body lengths 9.7
- replication (lineage window K = 20 frames = time 2000, default): splits 158, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 1, merges 246, merge/split ratio 1.56, nucleations 435
- channel total drift (end/start - 1): [-0.0455, None, -0.6134, -0.6022, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 34 at frame 62: holes 0, rim-vs-core 0.53, rim-vs-outside 0.15, heterogeneity 0.24; core [0.36, 0.577, 0.179, 0.43, 0.412] rim [0.311, 0.17, 0.193, 0.362, 0.09]
  - track 94 at frame 63: holes 0, rim-vs-core 0.43, rim-vs-outside 0.15, heterogeneity 0.17; core [0.304, 0.576, 0.176, 0.342, 0.279] rim [0.285, 0.194, 0.181, 0.314, 0.083]
  - track 112 at frame 64: holes 0, rim-vs-core 0.57, rim-vs-outside 0.17, heterogeneity 0.25; core [0.391, 0.604, 0.16, 0.457, 0.473] rim [0.332, 0.177, 0.175, 0.377, 0.111]
  - track 319 at frame 79: holes 0, rim-vs-core 0.55, rim-vs-outside 0.18, heterogeneity 0.26; core [0.432, 0.557, 0.153, 0.507, 0.462] rim [0.345, 0.167, 0.171, 0.397, 0.104]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1119 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.967, rim/outside 2.78 (aggregate of 1119 individuals; 84/1119 membrane-like individually; rim level 0.417)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.436, rim/outside 7.82 (aggregate of 1119 individuals; 13/1119 membrane-like individually; rim level 0.289)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.3, rim/outside 0.872 (aggregate of 1119 individuals; 0/1119 membrane-like individually; rim level 0.16)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.946, rim/outside 2.85 (aggregate of 1119 individuals; 55/1119 membrane-like individually; rim level 0.439)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.37, rim/outside 14 (aggregate of 1119 individuals; 14/1119 membrane-like individually; rim level 0.175)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #34 (t=6200, R_eq 4.33): none; #94 (t=6300, R_eq 4.03): none; #112 (t=6400, R_eq 4.37): none; #319 (t=7900, R_eq 4.26): none
- species `prey` (channels ['prey a'], own threshold): components final 177, mean 162.2, max 184; tracks 855, persistent 63; splits 57, persistent splits 14 (K=20), max generation 1, merges 38, merge/split 0.667; moving tracks 339
- species `predator` (channels ['predator b'], own threshold): components final 183, mean 142.5, max 196; tracks 735, persistent 60; splits 21, persistent splits 8 (K=20), max generation 1, merges 15, merge/split 0.714; moving tracks 311

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 1119 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
