# Evidence pack: digestion-driven-predators (seed 7)

- world: `../../../collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1744s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out c56work/lk/base256 --seeds 7 --size 256 256 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1564, 1.7968], min area 6 px

## Measurements
- components: final 189, mean 173.1, max 201; occupancy final 0.20
- tracks: 783; persistent (alive >= 50% of run): 74; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 22.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [196, 186, 155], H1 [0, 0, 0]
- motion: 310 long-lived tracks moved >= 1 body length; max speed 0.00801/time; max body lengths 8.9
- replication (lineage window K = 20 frames = time 2000, default): splits 144, persistent splits 45 (0 more failed only because the siblings re-merged within K), max generation 4, merges 167, merge/split ratio 1.16, nucleations 329
- channel total drift (end/start - 1): [-0.0514, None, -0.6128, -0.6006, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 62: holes 0, rim-vs-core 0.45, rim-vs-outside 0.17, heterogeneity 0.23; core [0.481, 0.46, 0.141, 0.538, 0.338] rim [0.361, 0.148, 0.162, 0.398, 0.076]
  - track 18 at frame 62: holes 0, rim-vs-core 0.47, rim-vs-outside 0.16, heterogeneity 0.27; core [0.444, 0.479, 0.147, 0.497, 0.374] rim [0.369, 0.137, 0.168, 0.405, 0.073]
  - track 39 at frame 62: holes 0, rim-vs-core 0.41, rim-vs-outside 0.13, heterogeneity 0.25; core [0.406, 0.468, 0.145, 0.435, 0.312] rim [0.305, 0.177, 0.169, 0.316, 0.063]
  - track 678 at frame 112: holes 0, rim-vs-core 0.43, rim-vs-outside 0.16, heterogeneity 0.25; core [0.396, 0.515, 0.158, 0.443, 0.305] rim [0.323, 0.181, 0.175, 0.355, 0.069]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1106 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.974, rim/outside 3.89 (aggregate of 1106 individuals; 149/1106 membrane-like individually; rim level 0.461)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.35, rim/outside 5.9 (aggregate of 1106 individuals; 15/1106 membrane-like individually; rim level 0.231)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.43, rim/outside 0.853 (aggregate of 1106 individuals; 0/1106 membrane-like individually; rim level 0.173)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.947, rim/outside 3.98 (aggregate of 1106 individuals; 87/1106 membrane-like individually; rim level 0.477)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.299, rim/outside 12.1 (aggregate of 1106 individuals; 16/1106 membrane-like individually; rim level 0.145)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #9 (t=6200, R_eq 4.11): none; #18 (t=6200, R_eq 4.69): none; #39 (t=6200, R_eq 4.92): none; #678 (t=11200, R_eq 4.62): none
- species `prey` (channels ['prey a'], own threshold): components final 183, mean 171.6, max 195; tracks 747, persistent 82; splits 144, persistent splits 62 (K=20), max generation 5, merges 57, merge/split 0.396; moving tracks 318
- species `predator` (channels ['predator b'], own threshold): components final 181, mean 143.5, max 191; tracks 605, persistent 75; splits 70, persistent splits 43 (K=20), max generation 4, merges 20, merge/split 0.286; moving tracks 299

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 1106 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
