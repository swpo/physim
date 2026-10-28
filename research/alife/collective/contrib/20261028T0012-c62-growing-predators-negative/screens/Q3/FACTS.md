# Evidence pack: growing-digestion-predators (seed 5)

- world: `../../c62work/world_grow.py`, family `active-emulsion`
- parent: collective/contrib/20261027T0325-c52-digestion-ecology-claim; mutation: predator fuel-depletion drift chiF 0.5 -> 0.25; before (c52): predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 266s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/c62work/world_grow.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/grow/Q3 --seeds 5 --size 128 128 --frames 80 --no-movie`
- segmentation: matter > 0.22 of robust range [0.1501, 1.7513], min area 6 px

## Measurements
- components: final 29, mean 39.0, max 63; occupancy final 0.31
- tracks: 203; persistent (alive >= 50% of run): 5; longest 48 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 41.10 (1 = constant size)
- enclosures: components with a hole mean 0.21, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 28, 12], H1 [1, 0, 0]
- motion: 22 long-lived tracks moved >= 1 body length; max speed 0.00721/time; max body lengths 2.4
- replication (lineage window K = 20 frames = time 2000, default): splits 45, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 22, merge/split ratio 0.489, nucleations 91
- channel total drift (end/start - 1): [0.1838, None, -0.6891, -0.5637, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 83 at frame 57: holes 0, rim-vs-core 0.14, rim-vs-outside 0.51, heterogeneity 0.05; core [0.812, 0.017, 0.011, 0.538, 0.005] rim [0.689, 0.012, 0.082, 0.543, 0.002]
  - track 84 at frame 57: holes 0, rim-vs-core 0.14, rim-vs-outside 0.45, heterogeneity 0.17; core [0.761, 0.082, 0.03, 0.539, 0.107] rim [0.642, 0.067, 0.084, 0.503, 0.06]
  - track 18 at frame 28: holes 0, rim-vs-core 0.21, rim-vs-outside 0.15, heterogeneity 0.22; core [0.445, 0.303, 0.218, 0.481, 0.127] rim [0.36, 0.158, 0.237, 0.383, 0.054]
  - track 139 at frame 65: holes 0, rim-vs-core 0.44, rim-vs-outside 0.19, heterogeneity 0.25; core [0.272, 0.561, 0.265, 0.299, 0.416] rim [0.254, 0.226, 0.27, 0.266, 0.139]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 235 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.961, rim/outside 3.17 (aggregate of 235 individuals; 63/235 membrane-like individually; rim level 0.433)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.543, rim/outside 6.64 (aggregate of 235 individuals; 9/235 membrane-like individually; rim level 0.232)
  - radial fuel F: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.31, rim/outside 0.914 (aggregate of 235 individuals; 0/235 membrane-like individually; rim level 0.251)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.965, rim/outside 3.13 (aggregate of 235 individuals; 61/235 membrane-like individually; rim level 0.415)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.484, rim/outside 7.87 (aggregate of 235 individuals; 9/235 membrane-like individually; rim level 0.124)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #83 (t=5700, R_eq 11.42): ['product p']; #84 (t=5700, R_eq 10.11): none; #18 (t=2800, R_eq 5.32): none; #139 (t=6500, R_eq 5.35): ['prey a', 'product p']
- species `prey` (channels ['prey a'], own threshold): components final 22, mean 34.6, max 45; tracks 214, persistent 3; splits 57, persistent splits 2 (K=20), max generation 1, merges 15, merge/split 0.263; moving tracks 22
- species `predator` (channels ['predator b'], own threshold): components final 21, mean 21.5, max 43; tracks 169, persistent 0; splits 28, persistent splits 0 (K=20), max generation 0, merges 3, merge/split 0.107; moving tracks 10

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 235 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
