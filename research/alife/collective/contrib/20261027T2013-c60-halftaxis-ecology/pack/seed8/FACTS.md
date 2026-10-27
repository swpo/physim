# Evidence pack: digestion-predators-half-taxis (seed 8)

- world: `../../world.py`, family `active-emulsion`
- parent: collective/contrib/20261027T0325-c52-digestion-ecology-claim; mutation: predator fuel-depletion drift chiF 0.5 -> 0.25; before (c52): predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1917s; status ok
- command: `python -m labkit.run collective/contrib/20261027T2013-c60-halftaxis-ecology/world.py --out collective/contrib/20261027T2013-c60-halftaxis-ecology/pack/seed8 --seeds 8 --size 256 256 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1578, 1.8074], min area 6 px

## Measurements
- components: final 171, mean 163.3, max 186; occupancy final 0.21
- tracks: 723; persistent (alive >= 50% of run): 54; longest 118 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 18.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [179, 172, 144], H1 [0, 0, 0]
- motion: 273 long-lived tracks moved >= 1 body length; max speed 0.00839/time; max body lengths 7.5
- replication (lineage window K = 20 frames = time 2000, default): splits 189, persistent splits 81 (0 more failed only because the siblings re-merged within K), max generation 4, merges 100, merge/split ratio 0.529, nucleations 247
- channel total drift (end/start - 1): [-0.0468, None, -0.6168, -0.6017, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 30 at frame 62: holes 0, rim-vs-core 0.42, rim-vs-outside 0.14, heterogeneity 0.23; core [0.361, 0.509, 0.183, 0.389, 0.286] rim [0.303, 0.169, 0.196, 0.317, 0.066]
  - track 59 at frame 62: holes 0, rim-vs-core 0.45, rim-vs-outside 0.17, heterogeneity 0.24; core [0.4, 0.512, 0.206, 0.465, 0.356] rim [0.327, 0.173, 0.223, 0.371, 0.089]
  - track 87 at frame 63: holes 0, rim-vs-core 0.43, rim-vs-outside 0.15, heterogeneity 0.26; core [0.436, 0.456, 0.183, 0.491, 0.327] rim [0.323, 0.155, 0.207, 0.357, 0.068]
  - track 491 at frame 101: holes 0, rim-vs-core 0.46, rim-vs-outside 0.14, heterogeneity 0.25; core [0.39, 0.509, 0.178, 0.428, 0.356] rim [0.324, 0.163, 0.197, 0.343, 0.072]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1029 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.978, rim/outside 4.85 (aggregate of 1029 individuals; 166/1029 membrane-like individually; rim level 0.475)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.35, rim/outside 4.85 (aggregate of 1029 individuals; 13/1029 membrane-like individually; rim level 0.216)
  - radial fuel F: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.47, rim/outside 0.853 (aggregate of 1029 individuals; 0/1029 membrane-like individually; rim level 0.198)
  - radial product p: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.956, rim/outside 4.83 (aggregate of 1029 individuals; 120/1029 membrane-like individually; rim level 0.486)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.29, rim/outside 10.8 (aggregate of 1029 individuals; 31/1029 membrane-like individually; rim level 0.133)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #30 (t=6200, R_eq 4.75): none; #59 (t=6200, R_eq 4.44): none; #87 (t=6300, R_eq 4.79): none; #491 (t=10100, R_eq 4.72): ['prey a']
- species `prey` (channels ['prey a'], own threshold): components final 171, mean 163.1, max 184; tracks 728, persistent 67; splits 208, persistent splits 93 (K=20), max generation 5, merges 45, merge/split 0.216; moving tracks 292
- species `predator` (channels ['predator b'], own threshold): components final 169, mean 133.8, max 178; tracks 600, persistent 52; splits 113, persistent splits 71 (K=20), max generation 3, merges 13, merge/split 0.115; moving tracks 303

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 1029 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
