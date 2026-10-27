# Evidence pack: digestion-driven-predators (seed 0)

- world: `../../../collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 438s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out c56work/ma/p0.45 --seeds 0 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1504, 1.7785], min area 6 px

## Measurements
- components: final 44, mean 38.3, max 50; occupancy final 0.16
- tracks: 129; persistent (alive >= 50% of run): 25; longest 118 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [44, 43, 35], H1 [0, 0, 0]
- motion: 70 long-lived tracks moved >= 1 body length; max speed 0.00807/time; max body lengths 9.2
- replication (lineage window K = 20 frames = time 2000, default): splits 14, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 1, merges 15, merge/split ratio 1.07, nucleations 86
- channel total drift (end/start - 1): [-0.0432, None, -0.58, -0.57, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 62: holes 0, rim-vs-core 0.59, rim-vs-outside 0.15, heterogeneity 0.23; core [0.317, 0.655, 0.185, 0.36, 0.44] rim [0.302, 0.168, 0.195, 0.33, 0.107]
  - track 9 at frame 62: holes 0, rim-vs-core 0.47, rim-vs-outside 0.18, heterogeneity 0.25; core [0.431, 0.514, 0.172, 0.494, 0.372] rim [0.316, 0.189, 0.196, 0.358, 0.09]
  - track 8 at frame 56: holes 0, rim-vs-core 0.63, rim-vs-outside 0.23, heterogeneity 0.26; core [0.614, 0.451, 0.103, 0.68, 0.563] rim [0.41, 0.118, 0.14, 0.449, 0.13]
  - track 33 at frame 78: holes 0, rim-vs-core 0.13, rim-vs-outside 0.41, heterogeneity 0.27; core [0.408, 0.442, 0.16, 0.452, 0.267] rim [0.411, 0.317, 0.157, 0.458, 0.274]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 251 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.977, rim/outside 3.69 (aggregate of 251 individuals; 27/251 membrane-like individually; rim level 0.432)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.386, rim/outside 6.05 (aggregate of 251 individuals; 0/251 membrane-like individually; rim level 0.27)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.35, rim/outside 0.857 (aggregate of 251 individuals; 0/251 membrane-like individually; rim level 0.189)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.954, rim/outside 3.82 (aggregate of 251 individuals; 17/251 membrane-like individually; rim level 0.458)
  - radial digestion q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.354, rim/outside 14.5 (aggregate of 251 individuals; 0/251 membrane-like individually; rim level 0.176)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=6200, R_eq 4.41): ['prey a']; #9 (t=6200, R_eq 4.41): none; #8 (t=5600, R_eq 4.3): none; #33 (t=7800, R_eq 4.51): none
- species `prey` (channels ['prey a'], own threshold): components final 41, mean 35.3, max 43; tracks 140, persistent 21; splits 14, persistent splits 9 (K=20), max generation 1, merges 2, merge/split 0.143; moving tracks 62
- species `predator` (channels ['predator b'], own threshold): components final 39, mean 31.2, max 43; tracks 128, persistent 18; splits 8, persistent splits 8 (K=20), max generation 1, merges 2, merge/split 0.25; moving tracks 60

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
