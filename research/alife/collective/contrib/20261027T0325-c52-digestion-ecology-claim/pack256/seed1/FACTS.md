# Evidence pack: digestion-driven-predators (seed 1)

- world: `../../world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1711s; status ok
- command: `python -m labkit.run c52work/world.py --out c52work/pack256/seed1 --seeds 1 --size 256 256 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1557, 1.7957], min area 6 px

## Measurements
- components: final 195, mean 172.2, max 201; occupancy final 0.19
- tracks: 783; persistent (alive >= 50% of run): 78; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 16.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [196, 184, 152], H1 [0, 0, 0]
- motion: 321 long-lived tracks moved >= 1 body length; max speed 0.00833/time; max body lengths 9.5
- replication (lineage window K = 20 frames = time 2000, default): splits 152, persistent splits 47 (0 more failed only because the siblings re-merged within K), max generation 3, merges 151, merge/split ratio 0.993, nucleations 329
- channel total drift (end/start - 1): [-0.0518, None, -0.6098, -0.5976, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 61: holes 0, rim-vs-core 0.32, rim-vs-outside 0.12, heterogeneity 0.19; core [0.383, 0.412, 0.15, 0.41, 0.2] rim [0.301, 0.159, 0.165, 0.317, 0.048]
  - track 47 at frame 62: holes 0, rim-vs-core 0.33, rim-vs-outside 0.11, heterogeneity 0.14; core [0.276, 0.506, 0.182, 0.294, 0.185] rim [0.255, 0.207, 0.189, 0.266, 0.057]
  - track 98 at frame 64: holes 0, rim-vs-core 0.48, rim-vs-outside 0.16, heterogeneity 0.23; core [0.387, 0.543, 0.169, 0.437, 0.353] rim [0.321, 0.168, 0.184, 0.353, 0.079]
  - track 524 at frame 99: holes 0, rim-vs-core 0.47, rim-vs-outside 0.15, heterogeneity 0.25; core [0.414, 0.502, 0.155, 0.465, 0.36] rim [0.331, 0.153, 0.176, 0.361, 0.071]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1111 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.966, rim/outside 3.87 (aggregate of 1111 individuals; 145/1111 membrane-like individually; rim level 0.451)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.355, rim/outside 5.82 (aggregate of 1111 individuals; 17/1111 membrane-like individually; rim level 0.236)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.42, rim/outside 0.854 (aggregate of 1111 individuals; 0/1111 membrane-like individually; rim level 0.177)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.939, rim/outside 3.96 (aggregate of 1111 individuals; 83/1111 membrane-like individually; rim level 0.469)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.301, rim/outside 12.2 (aggregate of 1111 individuals; 19/1111 membrane-like individually; rim level 0.147)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=6100, R_eq 4.41): none; #47 (t=6200, R_eq 4.03): none; #98 (t=6400, R_eq 4.37): none; #524 (t=9900, R_eq 4.58): none
- species `prey` (channels ['prey a'], own threshold): components final 193, mean 170.8, max 193; tracks 708, persistent 99; splits 141, persistent splits 69 (K=20), max generation 4, merges 46, merge/split 0.326; moving tracks 324
- species `predator` (channels ['predator b'], own threshold): components final 178, mean 142.7, max 189; tracks 600, persistent 74; splits 75, persistent splits 43 (K=20), max generation 3, merges 23, merge/split 0.307; moving tracks 313

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 1111 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
