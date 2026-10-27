# Evidence pack: digestion-driven-predators (seed 13)

- world: `../../20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1695s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out collective/contrib/c57-work/rerun --seeds 13 --size 256 256 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1591, 1.7955], min area 6 px

## Measurements
- components: final 191, mean 172.0, max 203; occupancy final 0.20
- tracks: 739; persistent (alive >= 50% of run): 83; longest 118 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 18.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [196, 190, 170], H1 [0, 0, 0]
- motion: 300 long-lived tracks moved >= 1 body length; max speed 0.00849/time; max body lengths 9.3
- replication (lineage window K = 20 frames = time 2000, default): splits 146, persistent splits 48 (0 more failed only because the siblings re-merged within K), max generation 3, merges 146, merge/split ratio 1, nucleations 303
- channel total drift (end/start - 1): [-0.0526, None, -0.6138, -0.6008, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 32 at frame 62: holes 0, rim-vs-core 0.50, rim-vs-outside 0.18, heterogeneity 0.25; core [0.443, 0.522, 0.156, 0.5, 0.418] rim [0.361, 0.163, 0.175, 0.396, 0.091]
  - track 33 at frame 62: holes 0, rim-vs-core 0.46, rim-vs-outside 0.15, heterogeneity 0.21; core [0.344, 0.561, 0.189, 0.387, 0.324] rim [0.3, 0.177, 0.198, 0.329, 0.083]
  - track 42 at frame 62: holes 0, rim-vs-core 0.49, rim-vs-outside 0.16, heterogeneity 0.26; core [0.515, 0.436, 0.119, 0.555, 0.381] rim [0.361, 0.143, 0.152, 0.379, 0.07]
  - track 469 at frame 96: holes 0, rim-vs-core 0.43, rim-vs-outside 0.15, heterogeneity 0.24; core [0.414, 0.497, 0.15, 0.455, 0.323] rim [0.338, 0.165, 0.167, 0.362, 0.074]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1105 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.98, rim/outside 4.01 (aggregate of 1105 individuals; 157/1105 membrane-like individually; rim level 0.454)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.344, rim/outside 6.01 (aggregate of 1105 individuals; 15/1105 membrane-like individually; rim level 0.231)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.42, rim/outside 0.855 (aggregate of 1105 individuals; 0/1105 membrane-like individually; rim level 0.177)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.952, rim/outside 4.09 (aggregate of 1105 individuals; 103/1105 membrane-like individually; rim level 0.47)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.293, rim/outside 12.1 (aggregate of 1105 individuals; 25/1105 membrane-like individually; rim level 0.144)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #32 (t=6200, R_eq 4.37): none; #33 (t=6200, R_eq 4.15): none; #42 (t=6200, R_eq 4.79): none; #469 (t=9600, R_eq 4.62): none
- species `prey` (channels ['prey a'], own threshold): components final 195, mean 172.6, max 195; tracks 743, persistent 97; splits 163, persistent splits 58 (K=20), max generation 3, merges 65, merge/split 0.399; moving tracks 302
- species `predator` (channels ['predator b'], own threshold): components final 184, mean 144.9, max 193; tracks 574, persistent 87; splits 76, persistent splits 38 (K=20), max generation 3, merges 22, merge/split 0.289; moving tracks 297

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 1105 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
