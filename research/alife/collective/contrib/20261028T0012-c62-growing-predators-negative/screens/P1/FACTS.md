# Evidence pack: growing-digestion-predators (seed 5)

- world: `../../c62work/world_grow.py`, family `active-emulsion`
- parent: collective/contrib/20261027T0325-c52-digestion-ecology-claim; mutation: predator fuel-depletion drift chiF 0.5 -> 0.25; before (c52): predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 266s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/c62work/world_grow.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/grow/P1 --seeds 5 --size 128 128 --frames 80 --no-movie`
- segmentation: matter > 0.22 of robust range [0.1501, 1.7467], min area 6 px

## Measurements
- components: final 23, mean 36.2, max 52; occupancy final 0.33
- tracks: 92; persistent (alive >= 50% of run): 30; longest 66 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 52.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 24, 22], H1 [1, 0, 0]
- motion: 29 long-lived tracks moved >= 1 body length; max speed 0.00689/time; max body lengths 3.3
- replication (lineage window K = 20 frames = time 2000, default): splits 13, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 9, merge/split ratio 0.692, nucleations 57
- channel total drift (end/start - 1): [0.3107, None, -0.7347, -0.5347, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 35: holes 0, rim-vs-core 0.45, rim-vs-outside 0.20, heterogeneity 0.22; core [0.729, 0.212, 0.13, 0.717, 0.269] rim [0.461, 0.095, 0.17, 0.448, 0.062]
  - track 31 at frame 36: holes 0, rim-vs-core 0.59, rim-vs-outside 0.17, heterogeneity 0.26; core [0.519, 0.463, 0.184, 0.54, 0.557] rim [0.385, 0.12, 0.207, 0.388, 0.115]
  - track 19 at frame 33: holes 0, rim-vs-core 0.58, rim-vs-outside 0.13, heterogeneity 0.24; core [0.429, 0.533, 0.19, 0.436, 0.535] rim [0.369, 0.147, 0.206, 0.361, 0.112]
  - track 85 at frame 67: holes 0, rim-vs-core 0.30, rim-vs-outside 0.44, heterogeneity 0.06; core [0.913, 0.028, 0.041, 0.747, 0.006] rim [0.677, 0.01, 0.101, 0.576, 0.001]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 222 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.914, rim/outside 3.87 (aggregate of 222 individuals; 23/222 membrane-like individually; rim level 0.584)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.49, rim/outside 8.54 (aggregate of 222 individuals; 4/222 membrane-like individually; rim level 0.186)
  - radial fuel F: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.66, rim/outside 0.875 (aggregate of 222 individuals; 0/222 membrane-like individually; rim level 0.21)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.934, rim/outside 3.97 (aggregate of 222 individuals; 18/222 membrane-like individually; rim level 0.532)
  - radial digestion q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.389, rim/outside 9.74 (aggregate of 222 individuals; 3/222 membrane-like individually; rim level 0.112)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=3500, R_eq 4.89): none; #31 (t=3600, R_eq 4.65): none; #19 (t=3300, R_eq 4.79): none; #85 (t=6700, R_eq 6.75): none
- species `prey` (channels ['prey a'], own threshold): components final 22, mean 36.0, max 53; tracks 129, persistent 15; splits 23, persistent splits 5 (K=20), max generation 2, merges 16, merge/split 0.696; moving tracks 25
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 14.5, max 42; tracks 72, persistent 1; splits 3, persistent splits 2 (K=20), max generation 1, merges 2, merge/split 0.667; moving tracks 23

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 222 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
