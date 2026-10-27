# Evidence pack: digestion-driven-predators (seed 0)

- world: `../../wswim.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 516s; status ok
- command: `python -m labkit.run c56work/wswim.py --out c56work/sw/w10 --seeds 0 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.26 of robust range [0.156, 1.4743], min area 6 px

## Measurements
- components: final 34, mean 36.7, max 51; occupancy final 0.11
- tracks: 205; persistent (alive >= 50% of run): 3; longest 64 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 18.25 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 23, 13], H1 [0, 0, 0]
- motion: 20 long-lived tracks moved >= 1 body length; max speed 0.00503/time; max body lengths 2.7
- replication (lineage window K = 20 frames = time 2000, default): splits 10, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 2, merge/split ratio 0.2, nucleations 183
- channel total drift (end/start - 1): [-0.0216, None, -0.6223, -0.6003, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 33 at frame 40: holes 0, rim-vs-core 0.39, rim-vs-outside 0.14, heterogeneity 0.13; core [0.472, 0.436, 0.133, 0.525, 0.253, 0.648] rim [0.287, 0.241, 0.16, 0.317, 0.069, 0.655]
  - track 3 at frame 32: holes 0, rim-vs-core 0.24, rim-vs-outside 0.11, heterogeneity 0.11; core [0.291, 0.482, 0.161, 0.309, 0.136, 0.576] rim [0.263, 0.262, 0.164, 0.275, 0.052, 0.577]
  - track 6 at frame 33: holes 0, rim-vs-core 0.16, rim-vs-outside 0.07, heterogeneity 0.09; core [0.272, 0.404, 0.16, 0.281, 0.081, 0.622] rim [0.245, 0.258, 0.165, 0.251, 0.041, 0.621]
  - track 38 at frame 50: holes 0, rim-vs-core 0.03, rim-vs-outside 0.03, heterogeneity 0.01; core [0.353, 0.174, 0.145, 0.367, 0.026, 0.625] rim [0.334, 0.172, 0.148, 0.346, 0.024, 0.625]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 225 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.8, rim/outside 3.04 (aggregate of 225 individuals; 0/225 membrane-like individually; rim level 0.459)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.596, rim/outside 3.14 (aggregate of 225 individuals; 0/225 membrane-like individually; rim level 0.315)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.52, rim/outside 0.873 (aggregate of 225 individuals; 0/225 membrane-like individually; rim level 0.165)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.792, rim/outside 3.12 (aggregate of 225 individuals; 0/225 membrane-like individually; rim level 0.474)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.395, rim/outside 8.75 (aggregate of 225 individuals; 0/225 membrane-like individually; rim level 0.133)
  - radial soluble predator u: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 0.992 (aggregate of 225 individuals; 0/225 membrane-like individually; rim level 0.612)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #33 (t=4000, R_eq 4.75): none; #3 (t=3200, R_eq 5.81): none; #6 (t=3300, R_eq 5.61): none; #38 (t=5000, R_eq 2.39): none
- species `prey` (channels ['prey a'], own threshold): components final 21, mean 23.3, max 43; tracks 221, persistent 0; splits 4, persistent splits 0 (K=20), max generation 0, merges 0, merge/split 0; moving tracks 11
- species `predator` (channels ['predator b'], own threshold): components final 18, mean 21.3, max 43; tracks 198, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 14

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
