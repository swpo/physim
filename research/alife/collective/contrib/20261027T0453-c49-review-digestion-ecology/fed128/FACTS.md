# Evidence pack: digestion-driven-predators (seed 4)

- world: `../../20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 71 frames x 500 steps x dt 0.2 = time 7000; grid [128, 128]; wall 229s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out collective/contrib/c49rev10/fed128 --seeds 4 --frames 70 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1532, 1.8002], min area 6 px

## Measurements
- components: final 49, mean 41.9, max 50; occupancy final 0.20
- tracks: 111; persistent (alive >= 50% of run): 29; longest 70 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 16.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [50, 45, 42], H1 [0, 0, 0]
- motion: 45 long-lived tracks moved >= 1 body length; max speed 0.00729/time; max body lengths 4.5
- replication (lineage window K = 20 frames = time 2000, default): splits 15, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 18, merge/split ratio 1.2, nucleations 63
- channel total drift (end/start - 1): [-0.0511, None, -0.6207, -0.6055, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 36: holes 0, rim-vs-core 0.46, rim-vs-outside 0.14, heterogeneity 0.27; core [0.456, 0.444, 0.153, 0.514, 0.36] rim [0.303, 0.171, 0.188, 0.334, 0.072]
  - track 3 at frame 36: holes 0, rim-vs-core 0.45, rim-vs-outside 0.14, heterogeneity 0.26; core [0.38, 0.502, 0.178, 0.437, 0.355] rim [0.296, 0.178, 0.2, 0.331, 0.072]
  - track 7 at frame 36: holes 0, rim-vs-core 0.57, rim-vs-outside 0.16, heterogeneity 0.24; core [0.448, 0.533, 0.139, 0.494, 0.459] rim [0.379, 0.11, 0.157, 0.406, 0.095]
  - track 48 at frame 51: holes 0, rim-vs-core 0.60, rim-vs-outside 0.21, heterogeneity 0.27; core [0.678, 0.325, 0.086, 0.722, 0.355] rim [0.317, 0.244, 0.152, 0.338, 0.096]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 272 components >= 12 px at frames [12, 23, 35, 47, 58, 70]):
  - radial prey a: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.945, rim/outside 4.23 (aggregate of 272 individuals; 32/272 membrane-like individually; rim level 0.485)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.353, rim/outside 5.5 (aggregate of 272 individuals; 3/272 membrane-like individually; rim level 0.231)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.51, rim/outside 0.847 (aggregate of 272 individuals; 0/272 membrane-like individually; rim level 0.177)
  - radial product p: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.922, rim/outside 4.32 (aggregate of 272 individuals; 13/272 membrane-like individually; rim level 0.51)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.342, rim/outside 15.9 (aggregate of 272 individuals; 3/272 membrane-like individually; rim level 0.191)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=3600, R_eq 5.05): none; #3 (t=3600, R_eq 4.85): none; #7 (t=3600, R_eq 4.33): none; #48 (t=5100, R_eq 4.79): none
- species `prey` (channels ['prey a'], own threshold): components final 50, mean 42.6, max 50; tracks 125, persistent 31; splits 22, persistent splits 7 (K=20), max generation 1, merges 7, merge/split 0.318; moving tracks 49
- species `predator` (channels ['predator b'], own threshold): components final 47, mean 29.7, max 49; tracks 95, persistent 24; splits 6, persistent splits 3 (K=20), max generation 1, merges 2, merge/split 0.333; moving tracks 46

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 272 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
