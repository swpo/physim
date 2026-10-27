# Evidence pack: digestion-driven-predators (seed 0)

- world: `../../wconv.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 439s; status ok
- command: `python -m labkit.run c56work/wconv.py --out c56work/cv/B4 --seeds 0 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.26 of robust range [0.156, 1.4803], min area 6 px

## Measurements
- components: final 42, mean 40.6, max 55; occupancy final 0.29
- tracks: 241; persistent (alive >= 50% of run): 6; longest 101 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.88 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [48, 48, 41], H1 [1, 0, 0]
- motion: 50 long-lived tracks moved >= 1 body length; max speed 0.00585/time; max body lengths 4.1
- replication (lineage window K = 20 frames = time 2000, default): splits 62, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 2, merges 46, merge/split ratio 0.742, nucleations 72
- channel total drift (end/start - 1): [-0.059, None, -0.6138, -0.6058, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 53: holes 0, rim-vs-core 0.52, rim-vs-outside 0.40, heterogeneity 0.20; core [0.204, 0.834, 0.23, 0.235, 0.383, 0.411] rim [0.305, 0.386, 0.215, 0.337, 0.167, 0.413]
  - track 80 at frame 82: holes 0, rim-vs-core 0.45, rim-vs-outside 0.18, heterogeneity 0.18; core [0.269, 0.677, 0.226, 0.297, 0.276, 0.405] rim [0.215, 0.28, 0.233, 0.232, 0.077, 0.407]
  - track 8 at frame 37: holes 0, rim-vs-core 0.49, rim-vs-outside 0.19, heterogeneity 0.19; core [0.255, 0.723, 0.206, 0.276, 0.313, 0.527] rim [0.199, 0.307, 0.213, 0.209, 0.078, 0.534]
  - track 169 at frame 104: holes 0, rim-vs-core 0.54, rim-vs-outside 0.32, heterogeneity 0.23; core [0.484, 0.642, 0.134, 0.523, 0.435, 0.381] rim [0.344, 0.294, 0.177, 0.367, 0.088, 0.394]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 260 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.999, rim/outside 4.15 (aggregate of 260 individuals; 79/260 membrane-like individually; rim level 0.425)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.506, rim/outside 5.06 (aggregate of 260 individuals; 1/260 membrane-like individually; rim level 0.337)
  - radial fuel F: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.41, rim/outside 0.888 (aggregate of 260 individuals; 0/260 membrane-like individually; rim level 0.196)
  - radial product p: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.975, rim/outside 4.11 (aggregate of 260 individuals; 63/260 membrane-like individually; rim level 0.426)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.405, rim/outside 8.85 (aggregate of 260 individuals; 7/260 membrane-like individually; rim level 0.147)
  - radial soluble predator u: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 0.996 (aggregate of 260 individuals; 0/260 membrane-like individually; rim level 0.373)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #15 (t=5300, R_eq 6.18): ['prey a', 'product p']; #80 (t=8200, R_eq 5.61): ['prey a', 'product p']; #8 (t=3700, R_eq 5.94): ['prey a', 'product p']; #169 (t=10400, R_eq 6.36): none
- species `prey` (channels ['prey a'], own threshold): components final 41, mean 39.7, max 49; tracks 181, persistent 15; splits 43, persistent splits 18 (K=20), max generation 3, merges 9, merge/split 0.209; moving tracks 70
- species `predator` (channels ['predator b'], own threshold): components final 44, mean 34.8, max 48; tracks 146, persistent 11; splits 31, persistent splits 17 (K=20), max generation 3, merges 5, merge/split 0.161; moving tracks 70

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 260 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
