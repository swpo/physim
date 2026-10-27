# Evidence pack: digestion-driven-predators (seed 9)

- world: `../../../collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 436s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out c56work/dh/full_s9 --seeds 9 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1559, 1.7935], min area 6 px

## Measurements
- components: final 48, mean 45.1, max 53; occupancy final 0.21
- tracks: 177; persistent (alive >= 50% of run): 22; longest 118 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [51, 48, 43], H1 [0, 0, 0]
- motion: 86 long-lived tracks moved >= 1 body length; max speed 0.00756/time; max body lengths 9.4
- replication (lineage window K = 20 frames = time 2000, default): splits 26, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 3, merges 38, merge/split ratio 1.46, nucleations 87
- channel total drift (end/start - 1): [-0.0565, None, -0.6117, -0.6006, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 61: holes 0, rim-vs-core 0.49, rim-vs-outside 0.18, heterogeneity 0.25; core [0.436, 0.523, 0.163, 0.504, 0.398] rim [0.347, 0.169, 0.181, 0.392, 0.095]
  - track 15 at frame 63: holes 0, rim-vs-core 0.40, rim-vs-outside 0.16, heterogeneity 0.23; core [0.423, 0.472, 0.144, 0.466, 0.283] rim [0.331, 0.162, 0.16, 0.358, 0.073]
  - track 20 at frame 63: holes 0, rim-vs-core 0.39, rim-vs-outside 0.15, heterogeneity 0.19; core [0.468, 0.436, 0.128, 0.512, 0.291] rim [0.363, 0.148, 0.144, 0.396, 0.073]
  - track 150 at frame 108: holes 0, rim-vs-core 0.49, rim-vs-outside 0.19, heterogeneity 0.27; core [0.517, 0.47, 0.107, 0.553, 0.411] rim [0.378, 0.16, 0.134, 0.393, 0.097]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 285 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.998, rim/outside 3.92 (aggregate of 285 individuals; 40/285 membrane-like individually; rim level 0.457)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.346, rim/outside 6.15 (aggregate of 285 individuals; 6/285 membrane-like individually; rim level 0.236)
  - radial fuel F: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.41, rim/outside 0.855 (aggregate of 285 individuals; 0/285 membrane-like individually; rim level 0.171)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.966, rim/outside 4 (aggregate of 285 individuals; 23/285 membrane-like individually; rim level 0.477)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.312, rim/outside 12.8 (aggregate of 285 individuals; 6/285 membrane-like individually; rim level 0.155)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=6100, R_eq 4.3): none; #15 (t=6300, R_eq 4.37): none; #20 (t=6300, R_eq 3.95): none; #150 (t=10800, R_eq 4.58): none
- species `prey` (channels ['prey a'], own threshold): components final 46, mean 44.9, max 52; tracks 158, persistent 29; splits 26, persistent splits 11 (K=20), max generation 3, merges 12, merge/split 0.462; moving tracks 79
- species `predator` (channels ['predator b'], own threshold): components final 46, mean 37.5, max 51; tracks 130, persistent 26; splits 11, persistent splits 8 (K=20), max generation 3, merges 5, merge/split 0.455; moving tracks 76

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 285 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
