# Evidence pack: digestion-driven-predators (seed 9)

- world: `../../../collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 1000 steps x dt 0.2 = time 24000; grid [128, 128]; wall 855s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out c56work/dh/half_s9 --seeds 9 --size 128 128 --frames 120 --spf 1000 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1558, 1.7974], min area 6 px

## Measurements
- components: final 45, mean 44.0, max 54; occupancy final 0.20
- tracks: 198; persistent (alive >= 50% of run): 18; longest 115 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.88 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [46, 46, 40], H1 [0, 0, 0]
- motion: 83 long-lived tracks moved >= 1 body length; max speed 0.00425/time; max body lengths 9.4
- replication (lineage window K = 20 frames = time 4000, default): splits 32, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 3, merges 47, merge/split ratio 1.47, nucleations 86
- channel total drift (end/start - 1): [-0.0574, None, -0.61, -0.6017, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 27 at frame 64: holes 0, rim-vs-core 0.45, rim-vs-outside 0.16, heterogeneity 0.23; core [0.418, 0.487, 0.164, 0.476, 0.328] rim [0.291, 0.178, 0.186, 0.327, 0.073]
  - track 36 at frame 65: holes 0, rim-vs-core 0.44, rim-vs-outside 0.13, heterogeneity 0.25; core [0.378, 0.495, 0.147, 0.409, 0.322] rim [0.293, 0.167, 0.166, 0.306, 0.068]
  - track 11 at frame 59: holes 0, rim-vs-core 0.43, rim-vs-outside 0.16, heterogeneity 0.26; core [0.445, 0.457, 0.145, 0.496, 0.326] rim [0.347, 0.157, 0.169, 0.379, 0.064]
  - track 160 at frame 110: holes 0, rim-vs-core 0.49, rim-vs-outside 0.18, heterogeneity 0.26; core [0.501, 0.481, 0.119, 0.553, 0.411] rim [0.361, 0.184, 0.148, 0.389, 0.095]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 280 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 0.985, rim/outside 3.67 (aggregate of 280 individuals; 36/280 membrane-like individually; rim level 0.441)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.359, rim/outside 6.24 (aggregate of 280 individuals; 3/280 membrane-like individually; rim level 0.239)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.39, rim/outside 0.855 (aggregate of 280 individuals; 0/280 membrane-like individually; rim level 0.17)
  - radial product p: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.952, rim/outside 3.74 (aggregate of 280 individuals; 22/280 membrane-like individually; rim level 0.456)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.301, rim/outside 11.8 (aggregate of 280 individuals; 6/280 membrane-like individually; rim level 0.138)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #27 (t=12800, R_eq 4.44): none; #36 (t=13000, R_eq 5.01): none; #11 (t=11800, R_eq 4.82): none; #160 (t=22000, R_eq 4.55): none
- species `prey` (channels ['prey a'], own threshold): components final 40, mean 43.7, max 52; tracks 159, persistent 25; splits 24, persistent splits 11 (K=20), max generation 3, merges 9, merge/split 0.375; moving tracks 81
- species `predator` (channels ['predator b'], own threshold): components final 45, mean 36.1, max 50; tracks 138, persistent 22; splits 12, persistent splits 6 (K=20), max generation 2, merges 3, merge/split 0.25; moving tracks 78

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 280 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
