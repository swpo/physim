# Evidence pack: digestion-driven-predators (seed 44)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 290s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out /tmp/claude-0/rev/lcut_s44b --seeds 44 --size 128 128 --frames 80 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1519, 1.8002], min area 6 px

## Measurements
- components: final 50, mean 42.0, max 51; occupancy final 0.20
- tracks: 112; persistent (alive >= 50% of run): 40; longest 78 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 19.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [48, 47, 42], H1 [0, 0, 0]
- motion: 52 long-lived tracks moved >= 1 body length; max speed 0.00827/time; max body lengths 5.2
- replication (lineage window K = 20 frames = time 2000, default): splits 18, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 14, merge/split ratio 0.778, nucleations 62
- channel total drift (end/start - 1): [-0.0512, None, -0.6236, -0.6099, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 42: holes 0, rim-vs-core 0.45, rim-vs-outside 0.17, heterogeneity 0.26; core [0.554, 0.391, 0.108, 0.59, 0.331] rim [0.385, 0.138, 0.146, 0.402, 0.061]
  - track 12 at frame 42: holes 0, rim-vs-core 0.19, rim-vs-outside 0.22, heterogeneity 0.16; core [0.316, 0.423, 0.203, 0.35, 0.159] rim [0.227, 0.311, 0.216, 0.251, 0.091]
  - track 15 at frame 42: holes 0, rim-vs-core 0.46, rim-vs-outside 0.15, heterogeneity 0.25; core [0.39, 0.527, 0.179, 0.446, 0.356] rim [0.315, 0.184, 0.198, 0.35, 0.084]
  - track 40 at frame 56: holes 0, rim-vs-core 0.50, rim-vs-outside 0.16, heterogeneity 0.25; core [0.42, 0.517, 0.182, 0.49, 0.4] rim [0.308, 0.167, 0.205, 0.351, 0.086]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 270 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 3.4 (aggregate of 270 individuals; 49/270 membrane-like individually; rim level 0.434)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.356, rim/outside 7.02 (aggregate of 270 individuals; 2/270 membrane-like individually; rim level 0.251)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.33, rim/outside 0.87 (aggregate of 270 individuals; 0/270 membrane-like individually; rim level 0.184)
  - radial product p: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.974, rim/outside 3.51 (aggregate of 270 individuals; 33/270 membrane-like individually; rim level 0.454)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.299, rim/outside 12.6 (aggregate of 270 individuals; 4/270 membrane-like individually; rim level 0.15)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=4200, R_eq 5.08): none; #12 (t=4200, R_eq 4.95): ['prey a']; #15 (t=4200, R_eq 4.51): none; #40 (t=5600, R_eq 4.55): none
- species `prey` (channels ['prey a'], own threshold): components final 45, mean 41.9, max 51; tracks 113, persistent 36; splits 17, persistent splits 6 (K=20), max generation 1, merges 7, merge/split 0.412; moving tracks 57
- species `predator` (channels ['predator b'], own threshold): components final 45, mean 31.8, max 49; tracks 90, persistent 31; splits 7, persistent splits 4 (K=20), max generation 1, merges 1, merge/split 0.143; moving tracks 51

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 270 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
