# Evidence pack: digestion-driven-predators (seed 5)

- world: `../../20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 235s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out collective/contrib/20261027T0545-c51-review-digestion/fed128_s5 --seeds 5 --size 128 128 --frames 80 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1501, 1.8009], min area 6 px

## Measurements
- components: final 48, mean 43.5, max 52; occupancy final 0.20
- tracks: 140; persistent (alive >= 50% of run): 31; longest 80 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 21.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [47, 45, 38], H1 [0, 0, 0]
- motion: 50 long-lived tracks moved >= 1 body length; max speed 0.00795/time; max body lengths 5.3
- replication (lineage window K = 20 frames = time 2000, default): splits 20, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 25, merge/split ratio 1.25, nucleations 75
- channel total drift (end/start - 1): [-0.0498, None, -0.6217, -0.6063, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 41: holes 0, rim-vs-core 0.33, rim-vs-outside 0.13, heterogeneity 0.21; core [0.396, 0.424, 0.147, 0.427, 0.213] rim [0.321, 0.168, 0.162, 0.337, 0.051]
  - track 6 at frame 42: holes 0, rim-vs-core 0.39, rim-vs-outside 0.13, heterogeneity 0.07; core [0.19, 0.594, 0.206, 0.197, 0.185] rim [0.213, 0.227, 0.205, 0.216, 0.064]
  - track 16 at frame 42: holes 0, rim-vs-core 0.25, rim-vs-outside 0.11, heterogeneity 0.08; core [0.144, 0.486, 0.239, 0.152, 0.097] rim [0.164, 0.249, 0.235, 0.17, 0.042]
  - track 58 at frame 57: holes 0, rim-vs-core 0.50, rim-vs-outside 0.17, heterogeneity 0.26; core [0.433, 0.514, 0.173, 0.503, 0.396] rim [0.326, 0.166, 0.196, 0.371, 0.087]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 279 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.977, rim/outside 3.33 (aggregate of 279 individuals; 43/279 membrane-like individually; rim level 0.441)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.373, rim/outside 6.96 (aggregate of 279 individuals; 4/279 membrane-like individually; rim level 0.249)
  - radial fuel F: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.39, rim/outside 0.867 (aggregate of 279 individuals; 0/279 membrane-like individually; rim level 0.176)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.954, rim/outside 3.42 (aggregate of 279 individuals; 26/279 membrane-like individually; rim level 0.46)
  - radial digestion q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.296, rim/outside 12 (aggregate of 279 individuals; 2/279 membrane-like individually; rim level 0.138)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=4100, R_eq 5.14): none; #6 (t=4200, R_eq 3.78): none; #16 (t=4200, R_eq 4.07): none; #58 (t=5700, R_eq 4.58): none
- species `prey` (channels ['prey a'], own threshold): components final 48, mean 43.3, max 51; tracks 142, persistent 30; splits 23, persistent splits 7 (K=20), max generation 2, merges 8, merge/split 0.348; moving tracks 56
- species `predator` (channels ['predator b'], own threshold): components final 44, mean 31.9, max 50; tracks 115, persistent 22; splits 11, persistent splits 3 (K=20), max generation 1, merges 4, merge/split 0.364; moving tracks 50

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
