# Evidence pack: digestion-driven-predators (seed 44)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 293s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out /tmp/claude-0/rev/lcut_s44a --seeds 44 --size 128 128 --frames 80 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1519, 1.7994], min area 6 px

## Measurements
- components: final 44, mean 41.7, max 51; occupancy final 0.20
- tracks: 106; persistent (alive >= 50% of run): 39; longest 78 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [49, 49, 40], H1 [0, 0, 0]
- motion: 52 long-lived tracks moved >= 1 body length; max speed 0.00823/time; max body lengths 5.3
- replication (lineage window K = 20 frames = time 2000, default): splits 15, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 16, merge/split ratio 1.07, nucleations 60
- channel total drift (end/start - 1): [-0.0524, None, -0.623, -0.6102, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 42: holes 0, rim-vs-core 0.45, rim-vs-outside 0.17, heterogeneity 0.26; core [0.554, 0.391, 0.106, 0.591, 0.33] rim [0.385, 0.138, 0.145, 0.402, 0.061]
  - track 12 at frame 42: holes 0, rim-vs-core 0.19, rim-vs-outside 0.22, heterogeneity 0.16; core [0.316, 0.423, 0.202, 0.35, 0.158] rim [0.227, 0.311, 0.215, 0.252, 0.09]
  - track 15 at frame 42: holes 0, rim-vs-core 0.45, rim-vs-outside 0.15, heterogeneity 0.25; core [0.39, 0.527, 0.178, 0.447, 0.355] rim [0.315, 0.184, 0.197, 0.351, 0.083]
  - track 40 at frame 56: holes 0, rim-vs-core 0.50, rim-vs-outside 0.16, heterogeneity 0.25; core [0.42, 0.517, 0.181, 0.491, 0.398] rim [0.308, 0.167, 0.204, 0.351, 0.086]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 266 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 3.4 (aggregate of 266 individuals; 45/266 membrane-like individually; rim level 0.431)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.365, rim/outside 7.31 (aggregate of 266 individuals; 4/266 membrane-like individually; rim level 0.254)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.33, rim/outside 0.871 (aggregate of 266 individuals; 0/266 membrane-like individually; rim level 0.184)
  - radial product p: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.978, rim/outside 3.5 (aggregate of 266 individuals; 36/266 membrane-like individually; rim level 0.452)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.311, rim/outside 13 (aggregate of 266 individuals; 7/266 membrane-like individually; rim level 0.153)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=4200, R_eq 5.08): none; #12 (t=4200, R_eq 4.95): ['prey a']; #15 (t=4200, R_eq 4.51): none; #40 (t=5600, R_eq 4.55): none
- species `prey` (channels ['prey a'], own threshold): components final 44, mean 41.8, max 51; tracks 113, persistent 37; splits 18, persistent splits 6 (K=20), max generation 1, merges 8, merge/split 0.444; moving tracks 55
- species `predator` (channels ['predator b'], own threshold): components final 48, mean 31.9, max 49; tracks 90, persistent 35; splits 7, persistent splits 4 (K=20), max generation 1, merges 1, merge/split 0.143; moving tracks 51

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 266 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
