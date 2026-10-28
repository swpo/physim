# Evidence pack: digestion-driven-predators (seed 83)

- world: `../../claim_world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 426s; status ok
- command: `python -m labkit.run collective/contrib/20261028T1015-c63-review-digestion-ecology/claim_world.py --out collective/contrib/20261028T1015-c63-review-digestion-ecology/rerun/seed83 --seeds 83 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1584, 1.7966], min area 6 px

## Measurements
- components: final 49, mean 43.0, max 51; occupancy final 0.20
- tracks: 215; persistent (alive >= 50% of run): 11; longest 87 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.31 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [49, 47, 38], H1 [0, 0, 0]
- motion: 84 long-lived tracks moved >= 1 body length; max speed 0.00826/time; max body lengths 6.4
- replication (lineage window K = 20 frames = time 2000, default): splits 43, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 50, merge/split ratio 1.16, nucleations 83
- channel total drift (end/start - 1): [-0.0522, None, -0.6172, -0.6049, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 57 at frame 78: holes 0, rim-vs-core 0.46, rim-vs-outside 0.15, heterogeneity 0.26; core [0.466, 0.459, 0.124, 0.504, 0.35] rim [0.342, 0.149, 0.153, 0.36, 0.063]
  - track 59 at frame 78: holes 0, rim-vs-core 0.46, rim-vs-outside 0.18, heterogeneity 0.24; core [0.41, 0.505, 0.166, 0.468, 0.343] rim [0.315, 0.167, 0.188, 0.352, 0.077]
  - track 20 at frame 46: holes 0, rim-vs-core 0.34, rim-vs-outside 0.14, heterogeneity 0.23; core [0.42, 0.426, 0.132, 0.448, 0.207] rim [0.329, 0.156, 0.153, 0.342, 0.047]
  - track 137 at frame 93: holes 0, rim-vs-core 0.44, rim-vs-outside 0.13, heterogeneity 0.21; core [0.343, 0.539, 0.177, 0.383, 0.305] rim [0.298, 0.177, 0.189, 0.322, 0.068]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 281 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.954, rim/outside 3.82 (aggregate of 281 individuals; 36/281 membrane-like individually; rim level 0.456)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.353, rim/outside 5.72 (aggregate of 281 individuals; 5/281 membrane-like individually; rim level 0.227)
  - radial fuel F: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.46, rim/outside 0.854 (aggregate of 281 individuals; 0/281 membrane-like individually; rim level 0.172)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.929, rim/outside 3.88 (aggregate of 281 individuals; 27/281 membrane-like individually; rim level 0.472)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.287, rim/outside 11.4 (aggregate of 281 individuals; 4/281 membrane-like individually; rim level 0.138)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #57 (t=7800, R_eq 4.98): none; #59 (t=7800, R_eq 4.58): none; #20 (t=4600, R_eq 5.2): ['prey a']; #137 (t=9300, R_eq 4.48): ['prey a']
- species `prey` (channels ['prey a'], own threshold): components final 44, mean 43.3, max 50; tracks 203, persistent 19; splits 46, persistent splits 18 (K=20), max generation 2, merges 17, merge/split 0.37; moving tracks 82
- species `predator` (channels ['predator b'], own threshold): components final 47, mean 35.8, max 50; tracks 159, persistent 17; splits 25, persistent splits 12 (K=20), max generation 2, merges 8, merge/split 0.32; moving tracks 83

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 281 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
