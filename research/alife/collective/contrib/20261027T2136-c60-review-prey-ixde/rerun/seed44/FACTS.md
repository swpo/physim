# Evidence pack: digestion-driven-predators (seed 44)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1755s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out /tmp/claude-0/rev/seed44 --seeds 44 --size 256 256 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1556, 1.7939], min area 6 px

## Measurements
- components: final 201, mean 174.8, max 201; occupancy final 0.20
- tracks: 777; persistent (alive >= 50% of run): 81; longest 117 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 25.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [203, 193, 158], H1 [0, 0, 0]
- motion: 323 long-lived tracks moved >= 1 body length; max speed 0.00849/time; max body lengths 9.1
- replication (lineage window K = 20 frames = time 2000, default): splits 137, persistent splits 31 (0 more failed only because the siblings re-merged within K), max generation 3, merges 164, merge/split ratio 1.2, nucleations 341
- channel total drift (end/start - 1): [-0.0528, None, -0.6132, -0.6, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 49 at frame 63: holes 0, rim-vs-core 0.48, rim-vs-outside 0.18, heterogeneity 0.26; core [0.493, 0.47, 0.145, 0.559, 0.374] rim [0.356, 0.158, 0.173, 0.402, 0.077]
  - track 54 at frame 63: holes 0, rim-vs-core 0.47, rim-vs-outside 0.15, heterogeneity 0.26; core [0.388, 0.511, 0.168, 0.442, 0.354] rim [0.327, 0.152, 0.185, 0.362, 0.074]
  - track 70 at frame 63: holes 0, rim-vs-core 0.40, rim-vs-outside 0.14, heterogeneity 0.26; core [0.411, 0.448, 0.144, 0.446, 0.298] rim [0.335, 0.151, 0.164, 0.354, 0.063]
  - track 644 at frame 110: holes 0, rim-vs-core 0.45, rim-vs-outside 0.16, heterogeneity 0.25; core [0.501, 0.45, 0.094, 0.521, 0.345] rim [0.414, 0.126, 0.117, 0.416, 0.065]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1117 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 0.96, rim/outside 3.92 (aggregate of 1117 individuals; 130/1117 membrane-like individually; rim level 0.458)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.35, rim/outside 5.93 (aggregate of 1117 individuals; 19/1117 membrane-like individually; rim level 0.232)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.45, rim/outside 0.851 (aggregate of 1117 individuals; 0/1117 membrane-like individually; rim level 0.17)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.93, rim/outside 4 (aggregate of 1117 individuals; 69/1117 membrane-like individually; rim level 0.475)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.297, rim/outside 12.3 (aggregate of 1117 individuals; 27/1117 membrane-like individually; rim level 0.147)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #49 (t=6300, R_eq 4.37): none; #54 (t=6300, R_eq 4.72): none; #70 (t=6300, R_eq 5.14): ['prey a', 'product p']; #644 (t=11000, R_eq 4.85): none
- species `prey` (channels ['prey a'], own threshold): components final 193, mean 174.3, max 200; tracks 729, persistent 96; splits 134, persistent splits 56 (K=20), max generation 3, merges 70, merge/split 0.522; moving tracks 331
- species `predator` (channels ['predator b'], own threshold): components final 185, mean 144.7, max 194; tracks 573, persistent 84; splits 60, persistent splits 37 (K=20), max generation 3, merges 20, merge/split 0.333; moving tracks 310

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 1117 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
