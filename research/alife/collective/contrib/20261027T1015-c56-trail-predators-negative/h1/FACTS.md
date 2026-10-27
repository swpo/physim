# Evidence pack: digestion-driven-predators (seed 0)

- world: `../../wswim.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 521s; status ok
- command: `python -m labkit.run c56work/wswim.py --out c56work/sw/h1 --seeds 0 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.30 of robust range [0.156, 1.2906], min area 6 px

## Measurements
- components: final 38, mean 36.1, max 38; occupancy final 0.22
- tracks: 38; persistent (alive >= 50% of run): 38; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 24.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 38, 38], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 38
- channel total drift (end/start - 1): [-0.0545, None, -0.6171, -0.6037, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 61: holes 0, rim-vs-core 0.74, rim-vs-outside 0.33, heterogeneity 0.15; core [0.78, 0.704, 0.038, 0.756, 0.495, 0.415] rim [0.377, 0.417, 0.113, 0.372, 0.107, 0.431]
  - track 1 at frame 62: holes 0, rim-vs-core 0.71, rim-vs-outside 0.20, heterogeneity 0.16; core [0.695, 0.671, 0.077, 0.705, 0.445, 0.406] rim [0.31, 0.397, 0.143, 0.324, 0.09, 0.419]
  - track 2 at frame 62: holes 0, rim-vs-core 0.69, rim-vs-outside 0.20, heterogeneity 0.16; core [0.699, 0.671, 0.074, 0.707, 0.447, 0.408] rim [0.323, 0.402, 0.139, 0.335, 0.095, 0.421]
  - track 3 at frame 62: holes 0, rim-vs-core 0.67, rim-vs-outside 0.18, heterogeneity 0.16; core [0.689, 0.647, 0.064, 0.68, 0.412, 0.415] rim [0.316, 0.391, 0.129, 0.319, 0.085, 0.428]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 226 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.704, rim/outside 9.79 (aggregate of 226 individuals; 0/226 membrane-like individually; rim level 0.67)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.602, rim/outside 2.16 (aggregate of 226 individuals; 0/226 membrane-like individually; rim level 0.479)
  - radial fuel F: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 5.58, rim/outside 0.797 (aggregate of 226 individuals; 0/226 membrane-like individually; rim level 0.178)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.689, rim/outside 10.6 (aggregate of 226 individuals; 0/226 membrane-like individually; rim level 0.659)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.319, rim/outside 15.6 (aggregate of 226 individuals; 0/226 membrane-like individually; rim level 0.236)
  - radial soluble predator u: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 0.985 (aggregate of 226 individuals; 0/226 membrane-like individually; rim level 0.36)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=6100, R_eq 6.15): none; #1 (t=6200, R_eq 5.56): none; #2 (t=6200, R_eq 5.56): none; #3 (t=6200, R_eq 5.75): none
- species `prey` (channels ['prey a'], own threshold): components final 38, mean 37.0, max 38; tracks 41, persistent 38; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 1
- species `predator` (channels ['predator b'], own threshold): components final 38, mean 31.1, max 38; tracks 38, persistent 38; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
