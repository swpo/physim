# Evidence pack: digestion-driven-predators (seed 44)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 295s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out /tmp/claude-0/rev/fed128_s44 --seeds 44 --size 128 128 --frames 80 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1519, 1.8026], min area 6 px

## Measurements
- components: final 46, mean 41.9, max 51; occupancy final 0.20
- tracks: 110; persistent (alive >= 50% of run): 39; longest 78 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [50, 49, 44], H1 [0, 0, 0]
- motion: 53 long-lived tracks moved >= 1 body length; max speed 0.00827/time; max body lengths 5.3
- replication (lineage window K = 20 frames = time 2000, default): splits 17, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 16, merge/split ratio 0.941, nucleations 60
- channel total drift (end/start - 1): [-0.0556, None, -0.6136, -0.603, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 42: holes 0, rim-vs-core 0.45, rim-vs-outside 0.17, heterogeneity 0.26; core [0.554, 0.389, 0.097, 0.59, 0.327] rim [0.385, 0.138, 0.136, 0.402, 0.06]
  - track 12 at frame 42: holes 0, rim-vs-core 0.19, rim-vs-outside 0.22, heterogeneity 0.16; core [0.316, 0.422, 0.193, 0.349, 0.156] rim [0.227, 0.31, 0.206, 0.251, 0.089]
  - track 15 at frame 42: holes 0, rim-vs-core 0.45, rim-vs-outside 0.15, heterogeneity 0.25; core [0.39, 0.525, 0.169, 0.446, 0.352] rim [0.315, 0.183, 0.188, 0.35, 0.082]
  - track 40 at frame 56: holes 0, rim-vs-core 0.50, rim-vs-outside 0.15, heterogeneity 0.25; core [0.42, 0.515, 0.172, 0.49, 0.395] rim [0.308, 0.167, 0.195, 0.35, 0.085]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 268 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 3.49 (aggregate of 268 individuals; 46/268 membrane-like individually; rim level 0.435)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.358, rim/outside 7.26 (aggregate of 268 individuals; 4/268 membrane-like individually; rim level 0.251)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.35, rim/outside 0.864 (aggregate of 268 individuals; 0/268 membrane-like individually; rim level 0.179)
  - radial product p: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.977, rim/outside 3.56 (aggregate of 268 individuals; 33/268 membrane-like individually; rim level 0.458)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.308, rim/outside 13.1 (aggregate of 268 individuals; 7/268 membrane-like individually; rim level 0.154)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=4200, R_eq 5.08): none; #12 (t=4200, R_eq 4.95): ['prey a']; #15 (t=4200, R_eq 4.51): none; #40 (t=5600, R_eq 4.55): none
- species `prey` (channels ['prey a'], own threshold): components final 46, mean 42.2, max 51; tracks 111, persistent 37; splits 17, persistent splits 6 (K=20), max generation 1, merges 8, merge/split 0.471; moving tracks 57
- species `predator` (channels ['predator b'], own threshold): components final 47, mean 32.1, max 49; tracks 89, persistent 35; splits 7, persistent splits 4 (K=20), max generation 1, merges 1, merge/split 0.143; moving tracks 52

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 268 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
