# Evidence pack: digestion-driven-predators (seed 4)

- world: `../../20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 71 frames x 500 steps x dt 0.2 = time 7000; grid [128, 128]; wall 232s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out collective/contrib/c49rev10/dfork128 --seeds 4 --frames 70 --no-movie`
- segmentation: matter > 0.28 of robust range [0.0065, 1.7847], min area 6 px

## Measurements
- components: final 0, mean 36.9, max 50; occupancy final 0.00
- tracks: 102; persistent (alive >= 50% of run): 21; longest 63 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 19.43 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [41, 35, 10], H1 [2, 0, 0]
- motion: 36 long-lived tracks moved >= 1 body length; max speed 0.0073/time; max body lengths 3.6
- replication (lineage window K = 20 frames = time 2000, default): splits 13, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 16, merge/split ratio 1.23, nucleations 60
- channel total drift (end/start - 1): [-0.9999, None, 0.0, -1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 32: holes 0, rim-vs-core 0.40, rim-vs-outside 0.14, heterogeneity 0.25; core [0.548, 0.438, 0.144, 0.536, 0.306] rim [0.448, 0.165, 0.171, 0.409, 0.064]
  - track 7 at frame 33: holes 0, rim-vs-core 0.34, rim-vs-outside 0.12, heterogeneity 0.19; core [0.643, 0.276, 0.094, 0.622, 0.183] rim [0.459, 0.166, 0.131, 0.406, 0.039]
  - track 3 at frame 33: holes 0, rim-vs-core 0.43, rim-vs-outside 0.13, heterogeneity 0.25; core [0.478, 0.507, 0.176, 0.464, 0.336] rim [0.421, 0.181, 0.194, 0.383, 0.069]
  - track 49 at frame 48: holes 0, rim-vs-core 0.16, rim-vs-outside 0.39, heterogeneity 0.22; core [0.56, 0.395, 0.164, 0.571, 0.314] rim [0.473, 0.355, 0.181, 0.46, 0.246]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 223 components >= 12 px at frames [12, 23, 35, 47, 58]):
  - radial prey a: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.956, rim/outside 2.2 (aggregate of 223 individuals; 4/223 membrane-like individually; rim level 0.599)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.362, rim/outside 5.48 (aggregate of 223 individuals; 2/223 membrane-like individually; rim level 0.231)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.56, rim/outside 0.835 (aggregate of 223 individuals; 0/223 membrane-like individually; rim level 0.174)
  - radial product p: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.929, rim/outside 2.98 (aggregate of 223 individuals; 6/223 membrane-like individually; rim level 0.577)
  - radial digestion q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.372, rim/outside 17.4 (aggregate of 223 individuals; 3/223 membrane-like individually; rim level 0.212)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=3200, R_eq 5.32): none; #7 (t=3300, R_eq 5.14): none; #3 (t=3300, R_eq 5.11): none; #49 (t=4800, R_eq 4.11): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 37.1, max 50; tracks 239, persistent 13; splits 72, persistent splits 2 (K=20), max generation 1, merges 43, merge/split 0.597; moving tracks 31
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 25.4, max 49; tracks 85, persistent 16; splits 5, persistent splits 3 (K=20), max generation 1, merges 2, merge/split 0.4; moving tracks 43

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 223 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
