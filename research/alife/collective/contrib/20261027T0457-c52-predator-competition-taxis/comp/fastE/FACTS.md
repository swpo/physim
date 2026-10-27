# Evidence pack: digestion-predators-competition (seed 0)

- world: `../../world2p.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 101 frames x 500 steps x dt 0.2 = time 10000; grid [128, 128]; wall 496s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0457-c52-predator-competition-taxis/world2p.py --out collective/contrib/20261027T0457-c52-predator-competition-taxis/comp/fastE --seeds 0 --size 128 128 --frames 100 --no-movie`
- segmentation: matter > 0.20 of robust range [0.152, 1.9116], min area 6 px

## Measurements
- components: final 48, mean 42.2, max 51; occupancy final 0.17
- tracks: 135; persistent (alive >= 50% of run): 29; longest 98 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 22.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [47, 41, 29], H1 [0, 0, 0]
- motion: 69 long-lived tracks moved >= 1 body length; max speed 0.00806/time; max body lengths 5.9
- replication (lineage window K = 20 frames = time 2000, default): splits 25, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 2, merges 18, merge/split ratio 0.72, nucleations 67
- channel total drift (end/start - 1): [-0.0385, None, -0.6202, -0.6017, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 52: holes 0, rim-vs-core 0.63, rim-vs-outside 0.17, heterogeneity 0.24; core [0.43, 0.513, 0.163, 0.495, 0.349, 0.364, 0.389] rim [0.345, 0.181, 0.181, 0.387, 0.089, 0.052, 0.074]
  - track 14 at frame 52: holes 0, rim-vs-core 0.60, rim-vs-outside 0.31, heterogeneity 0.21; core [0.39, 0.272, 0.167, 0.452, 0.192, 0.641, 0.502] rim [0.422, 0.097, 0.168, 0.477, 0.077, 0.198, 0.154]
  - track 30 at frame 54: holes 0, rim-vs-core 0.60, rim-vs-outside 0.19, heterogeneity 0.21; core [0.536, 0.245, 0.131, 0.603, 0.194, 0.468, 0.501] rim [0.374, 0.066, 0.159, 0.414, 0.035, 0.165, 0.123]
  - track 98 at frame 85: holes 0, rim-vs-core 0.64, rim-vs-outside 0.19, heterogeneity 0.21; core [0.502, 0.496, 0.146, 0.574, 0.546, 0.27, 0.108] rim [0.356, 0.106, 0.172, 0.399, 0.116, 0.159, 0.033]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 263 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.892, rim/outside 3.94 (aggregate of 263 individuals; 9/263 membrane-like individually; rim level 0.496)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.362, rim/outside 5.03 (aggregate of 263 individuals; 3/263 membrane-like individually; rim level 0.162)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.52, rim/outside 0.849 (aggregate of 263 individuals; 0/263 membrane-like individually; rim level 0.172)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.879, rim/outside 4.08 (aggregate of 263 individuals; 8/263 membrane-like individually; rim level 0.525)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.34, rim/outside 11.1 (aggregate of 263 individuals; 3/263 membrane-like individually; rim level 0.122)
  - radial predator e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.398, rim/outside 4.81 (aggregate of 263 individuals; 3/263 membrane-like individually; rim level 0.186)
  - radial digestion q2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.322, rim/outside 11.3 (aggregate of 263 individuals; 5/263 membrane-like individually; rim level 0.128)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=5200, R_eq 4.26): none; #14 (t=5200, R_eq 4.18): none; #30 (t=5400, R_eq 4.11): none; #98 (t=8500, R_eq 4.26): none
- species `prey` (channels ['prey a'], own threshold): components final 41, mean 40.9, max 49; tracks 138, persistent 22; splits 20, persistent splits 12 (K=20), max generation 2, merges 3, merge/split 0.15; moving tracks 73
- species `predator` (channels ['predator b'], own threshold): components final 23, mean 16.7, max 27; tracks 150, persistent 1; splits 3, persistent splits 0 (K=20), max generation 0, merges 0, merge/split 0; moving tracks 12
- species `predator_e` (channels ['predator e'], own threshold): components final 26, mean 20.3, max 31; tracks 165, persistent 1; splits 1, persistent splits 0 (K=20), max generation 0, merges 0, merge/split 0; moving tracks 35

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
