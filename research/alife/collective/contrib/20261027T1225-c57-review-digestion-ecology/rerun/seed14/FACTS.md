# Evidence pack: digestion-driven-predators (seed 14)

- world: `../../20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1769s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out collective/contrib/c57-work/rerun14 --seeds 14 --size 256 256 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1572, 1.7943], min area 6 px

## Measurements
- components: final 193, mean 172.8, max 198; occupancy final 0.20
- tracks: 813; persistent (alive >= 50% of run): 70; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [198, 187, 150], H1 [0, 0, 0]
- motion: 312 long-lived tracks moved >= 1 body length; max speed 0.0083/time; max body lengths 8.3
- replication (lineage window K = 20 frames = time 2000, default): splits 161, persistent splits 49 (0 more failed only because the siblings re-merged within K), max generation 4, merges 173, merge/split ratio 1.07, nucleations 319
- channel total drift (end/start - 1): [-0.0502, None, -0.6156, -0.6019, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 62: holes 0, rim-vs-core 0.54, rim-vs-outside 0.15, heterogeneity 0.26; core [0.403, 0.539, 0.158, 0.456, 0.428] rim [0.349, 0.139, 0.177, 0.381, 0.085]
  - track 30 at frame 62: holes 0, rim-vs-core 0.43, rim-vs-outside 0.17, heterogeneity 0.25; core [0.482, 0.453, 0.136, 0.528, 0.333] rim [0.348, 0.164, 0.16, 0.375, 0.082]
  - track 69 at frame 63: holes 0, rim-vs-core 0.48, rim-vs-outside 0.16, heterogeneity 0.20; core [0.29, 0.622, 0.192, 0.318, 0.347] rim [0.269, 0.209, 0.199, 0.285, 0.099]
  - track 550 at frame 103: holes 0, rim-vs-core 0.48, rim-vs-outside 0.15, heterogeneity 0.26; core [0.435, 0.488, 0.15, 0.486, 0.38] rim [0.33, 0.154, 0.174, 0.36, 0.08]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1099 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.97, rim/outside 4.14 (aggregate of 1099 individuals; 132/1099 membrane-like individually; rim level 0.468)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.344, rim/outside 5.96 (aggregate of 1099 individuals; 14/1099 membrane-like individually; rim level 0.227)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.46, rim/outside 0.848 (aggregate of 1099 individuals; 0/1099 membrane-like individually; rim level 0.173)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.941, rim/outside 4.21 (aggregate of 1099 individuals; 88/1099 membrane-like individually; rim level 0.484)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.291, rim/outside 12.4 (aggregate of 1099 individuals; 15/1099 membrane-like individually; rim level 0.145)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #21 (t=6200, R_eq 4.65): none; #30 (t=6200, R_eq 4.41): none; #69 (t=6300, R_eq 4.37): none; #550 (t=10300, R_eq 4.82): none
- species `prey` (channels ['prey a'], own threshold): components final 180, mean 171.7, max 195; tracks 735, persistent 81; splits 151, persistent splits 70 (K=20), max generation 4, merges 65, merge/split 0.43; moving tracks 338
- species `predator` (channels ['predator b'], own threshold): components final 178, mean 142.8, max 189; tracks 613, persistent 71; splits 88, persistent splits 52 (K=20), max generation 4, merges 19, merge/split 0.216; moving tracks 309

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 1099 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
