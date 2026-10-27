# Evidence pack: digestion-driven-predators (seed 7)

- world: `../../../collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 286s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out c56work/py/ffork128_s7 --seeds 7 --size 128 128 --frames 80 --no-movie`
- segmentation: matter > 0.22 of robust range [0.1496, 1.768], min area 6 px

## Measurements
- components: final 27, mean 39.3, max 49; occupancy final 0.05
- tracks: 110; persistent (alive >= 50% of run): 28; longest 80 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 22.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 22, 7], H1 [0, 0, 0]
- motion: 41 long-lived tracks moved >= 1 body length; max speed 0.00745/time; max body lengths 3.6
- replication (lineage window K = 20 frames = time 2000, default): splits 16, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 18, merge/split ratio 1.12, nucleations 60
- channel total drift (end/start - 1): [-0.0083, None, -1.0, -1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 41: holes 0, rim-vs-core 0.56, rim-vs-outside 0.26, heterogeneity 0.25; core [0.306, 0.618, 0.391, 0.414, 0.418] rim [0.378, 0.172, 0.385, 0.477, 0.101]
  - track 9 at frame 42: holes 0, rim-vs-core 0.54, rim-vs-outside 0.16, heterogeneity 0.26; core [0.499, 0.496, 0.334, 0.587, 0.468] rim [0.355, 0.16, 0.358, 0.435, 0.102]
  - track 16 at frame 42: holes 0, rim-vs-core 0.47, rim-vs-outside 0.14, heterogeneity 0.26; core [0.435, 0.508, 0.356, 0.534, 0.394] rim [0.334, 0.183, 0.373, 0.425, 0.087]
  - track 61 at frame 57: holes 0, rim-vs-core 0.39, rim-vs-outside 0.12, heterogeneity 0.16; core [0.281, 0.547, 0.382, 0.366, 0.246] rim [0.278, 0.202, 0.387, 0.356, 0.069]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 238 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.97, rim/outside 2.49 (aggregate of 238 individuals; 29/238 membrane-like individually; rim level 0.383)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.462, rim/outside 6.69 (aggregate of 238 individuals; 2/238 membrane-like individually; rim level 0.297)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.09, rim/outside 0.939 (aggregate of 238 individuals; 0/238 membrane-like individually; rim level 0.263)
  - radial product p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.927, rim/outside 2.5 (aggregate of 238 individuals; 5/238 membrane-like individually; rim level 0.372)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.351, rim/outside 11.2 (aggregate of 238 individuals; 2/238 membrane-like individually; rim level 0.139)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=4100, R_eq 4.95): ['prey a']; #9 (t=4200, R_eq 4.69): none; #16 (t=4200, R_eq 4.69): none; #61 (t=5700, R_eq 4.41): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 29.3, max 48; tracks 106, persistent 13; splits 13, persistent splits 2 (K=20), max generation 1, merges 6, merge/split 0.462; moving tracks 41
- species `predator` (channels ['predator b'], own threshold): components final 5, mean 25.6, max 46; tracks 86, persistent 13; splits 5, persistent splits 3 (K=20), max generation 1, merges 2, merge/split 0.4; moving tracks 43

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
