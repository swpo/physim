# Evidence pack: digestion-driven-predators (seed 9)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1915s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/dig/pack256 --seeds 9 --size 256 256 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1576, 1.7974], min area 6 px

## Measurements
- components: final 193, mean 174.9, max 205; occupancy final 0.21
- tracks: 799; persistent (alive >= 50% of run): 76; longest 117 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 25.89 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [203, 191, 156], H1 [0, 0, 0]
- motion: 321 long-lived tracks moved >= 1 body length; max speed 0.00831/time; max body lengths 9.0
- replication (lineage window K = 20 frames = time 2000, default): splits 144, persistent splits 40 (0 more failed only because the siblings re-merged within K), max generation 3, merges 176, merge/split ratio 1.22, nucleations 337
- channel total drift (end/start - 1): [-0.0531, None, -0.6168, -0.6034, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 70 at frame 63: holes 0, rim-vs-core 0.40, rim-vs-outside 0.14, heterogeneity 0.24; core [0.416, 0.467, 0.141, 0.45, 0.283] rim [0.341, 0.159, 0.16, 0.359, 0.059]
  - track 95 at frame 64: holes 0, rim-vs-core 0.44, rim-vs-outside 0.16, heterogeneity 0.20; core [0.343, 0.557, 0.186, 0.391, 0.288] rim [0.319, 0.176, 0.193, 0.355, 0.078]
  - track 106 at frame 64: holes 0, rim-vs-core 0.47, rim-vs-outside 0.13, heterogeneity 0.18; core [0.257, 0.619, 0.203, 0.286, 0.289] rim [0.264, 0.194, 0.206, 0.282, 0.081]
  - track 523 at frame 99: holes 0, rim-vs-core 0.41, rim-vs-outside 0.14, heterogeneity 0.25; core [0.414, 0.468, 0.139, 0.448, 0.292] rim [0.358, 0.142, 0.157, 0.376, 0.058]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1123 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.963, rim/outside 3.87 (aggregate of 1123 individuals; 132/1123 membrane-like individually; rim level 0.456)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.356, rim/outside 6.17 (aggregate of 1123 individuals; 20/1123 membrane-like individually; rim level 0.235)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.43, rim/outside 0.855 (aggregate of 1123 individuals; 0/1123 membrane-like individually; rim level 0.174)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.937, rim/outside 3.93 (aggregate of 1123 individuals; 87/1123 membrane-like individually; rim level 0.473)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.296, rim/outside 12.1 (aggregate of 1123 individuals; 22/1123 membrane-like individually; rim level 0.145)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #70 (t=6300, R_eq 5.05): none; #95 (t=6400, R_eq 3.99): none; #106 (t=6400, R_eq 4.18): ['prey a', 'product p']; #523 (t=9900, R_eq 5.05): none
- species `prey` (channels ['prey a'], own threshold): components final 189, mean 174.8, max 202; tracks 765, persistent 84; splits 144, persistent splits 62 (K=20), max generation 3, merges 79, merge/split 0.549; moving tracks 332
- species `predator` (channels ['predator b'], own threshold): components final 190, mean 144.7, max 195; tracks 608, persistent 75; splits 68, persistent splits 38 (K=20), max generation 2, merges 23, merge/split 0.338; moving tracks 314

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 1123 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
