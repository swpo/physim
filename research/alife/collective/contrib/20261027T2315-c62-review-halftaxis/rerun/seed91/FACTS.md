# Evidence pack: digestion-predators-half-taxis (seed 91)

- world: `../../../20261027T2013-c60-halftaxis-ecology/world.py`, family `active-emulsion`
- parent: collective/contrib/20261027T0325-c52-digestion-ecology-claim; mutation: predator fuel-depletion drift chiF 0.5 -> 0.25; before (c52): predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1723s; status ok
- command: `python -m labkit.run collective/contrib/20261027T2013-c60-halftaxis-ecology/world.py --out collective/contrib/20261027T2315-c62-review-halftaxis/rerun/seed91 --seeds 91 --size 256 256 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1571, 1.8123], min area 6 px

## Measurements
- components: final 181, mean 163.7, max 193; occupancy final 0.21
- tracks: 737; persistent (alive >= 50% of run): 50; longest 118 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 16.86 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [186, 173, 137], H1 [0, 0, 0]
- motion: 275 long-lived tracks moved >= 1 body length; max speed 0.00766/time; max body lengths 7.5
- replication (lineage window K = 20 frames = time 2000, default): splits 187, persistent splits 78 (0 more failed only because the siblings re-merged within K), max generation 4, merges 103, merge/split ratio 0.551, nucleations 262
- channel total drift (end/start - 1): [-0.0498, None, -0.6149, -0.6009, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 24 at frame 62: holes 0, rim-vs-core 0.50, rim-vs-outside 0.19, heterogeneity 0.26; core [0.525, 0.435, 0.122, 0.563, 0.39] rim [0.379, 0.125, 0.153, 0.398, 0.068]
  - track 31 at frame 62: holes 0, rim-vs-core 0.23, rim-vs-outside 0.12, heterogeneity 0.16; core [0.376, 0.361, 0.184, 0.408, 0.103] rim [0.27, 0.209, 0.203, 0.291, 0.037]
  - track 51 at frame 63: holes 0, rim-vs-core 0.29, rim-vs-outside 0.14, heterogeneity 0.21; core [0.441, 0.371, 0.158, 0.478, 0.161] rim [0.327, 0.172, 0.179, 0.35, 0.044]
  - track 486 at frame 98: holes 0, rim-vs-core 0.37, rim-vs-outside 0.16, heterogeneity 0.18; core [0.55, 0.211, 0.13, 0.578, 0.049] rim [0.3, 0.172, 0.169, 0.319, 0.021]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1045 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.944, rim/outside 4.88 (aggregate of 1045 individuals; 117/1045 membrane-like individually; rim level 0.476)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.35, rim/outside 4.74 (aggregate of 1045 individuals; 19/1045 membrane-like individually; rim level 0.215)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.52, rim/outside 0.85 (aggregate of 1045 individuals; 0/1045 membrane-like individually; rim level 0.194)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.923, rim/outside 4.91 (aggregate of 1045 individuals; 89/1045 membrane-like individually; rim level 0.487)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.28, rim/outside 10.8 (aggregate of 1045 individuals; 28/1045 membrane-like individually; rim level 0.132)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #24 (t=6200, R_eq 4.79): none; #31 (t=6200, R_eq 4.26): none; #51 (t=6300, R_eq 4.55): none; #486 (t=9800, R_eq 5.05): none
- species `prey` (channels ['prey a'], own threshold): components final 171, mean 162.6, max 185; tracks 755, persistent 54; splits 205, persistent splits 98 (K=20), max generation 5, merges 50, merge/split 0.244; moving tracks 307
- species `predator` (channels ['predator b'], own threshold): components final 167, mean 133.1, max 178; tracks 620, persistent 56; splits 126, persistent splits 76 (K=20), max generation 5, merges 14, merge/split 0.111; moving tracks 300

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 1045 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
