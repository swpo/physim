# Evidence pack: digestion-predators-competition (seed 0)

- world: `../../world2p.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 101 frames x 500 steps x dt 0.2 = time 10000; grid [128, 128]; wall 489s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0457-c52-predator-competition-taxis/world2p.py --out collective/contrib/20261027T0457-c52-predator-competition-taxis/comp/halfE --seeds 0 --size 128 128 --frames 100 --no-movie`
- segmentation: matter > 0.19 of robust range [0.152, 1.974], min area 6 px

## Measurements
- components: final 48, mean 41.0, max 50; occupancy final 0.21
- tracks: 143; persistent (alive >= 50% of run): 22; longest 99 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 18.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [50, 47, 37], H1 [0, 0, 0]
- motion: 59 long-lived tracks moved >= 1 body length; max speed 0.00735/time; max body lengths 6.5
- replication (lineage window K = 20 frames = time 2000, default): splits 37, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 3, merges 15, merge/split ratio 0.405, nucleations 55
- channel total drift (end/start - 1): [-0.0429, None, -0.6201, -0.6018, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 51: holes 0, rim-vs-core 0.60, rim-vs-outside 0.14, heterogeneity 0.17; core [0.397, 0.551, 0.192, 0.447, 0.484, 0.155, 0.047] rim [0.299, 0.126, 0.211, 0.326, 0.091, 0.088, 0.018]
  - track 7 at frame 52: holes 0, rim-vs-core 0.48, rim-vs-outside 0.27, heterogeneity 0.09; core [0.854, 0.081, 0.039, 0.846, 0.055, 0.113, 0.07] rim [0.523, 0.021, 0.098, 0.522, 0.007, 0.059, 0.016]
  - track 19 at frame 52: holes 0, rim-vs-core 0.51, rim-vs-outside 0.16, heterogeneity 0.20; core [0.547, 0.373, 0.132, 0.597, 0.371, 0.122, 0.047] rim [0.352, 0.113, 0.175, 0.378, 0.056, 0.061, 0.011]
  - track 98 at frame 88: holes 0, rim-vs-core 0.62, rim-vs-outside 0.19, heterogeneity 0.21; core [0.492, 0.113, 0.154, 0.544, 0.045, 0.514, 0.586] rim [0.337, 0.053, 0.182, 0.365, 0.011, 0.161, 0.14]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 258 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.93, rim/outside 4.53 (aggregate of 258 individuals; 25/258 membrane-like individually; rim level 0.487)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.326, rim/outside 6.52 (aggregate of 258 individuals; 7/258 membrane-like individually; rim level 0.155)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.51, rim/outside 0.855 (aggregate of 258 individuals; 0/258 membrane-like individually; rim level 0.195)
  - radial product p: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.916, rim/outside 4.59 (aggregate of 258 individuals; 23/258 membrane-like individually; rim level 0.503)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.271, rim/outside 9.69 (aggregate of 258 individuals; 7/258 membrane-like individually; rim level 0.102)
  - radial predator e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.493, rim/outside 3.15 (aggregate of 258 individuals; 4/258 membrane-like individually; rim level 0.13)
  - radial digestion q2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.429, rim/outside 7.11 (aggregate of 258 individuals; 12/258 membrane-like individually; rim level 0.0781)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=5100, R_eq 4.26): none; #7 (t=5200, R_eq 5.14): none; #19 (t=5200, R_eq 5.2): none; #98 (t=8800, R_eq 4.75): none
- species `prey` (channels ['prey a'], own threshold): components final 45, mean 41.3, max 49; tracks 160, persistent 21; splits 41, persistent splits 19 (K=20), max generation 2, merges 8, merge/split 0.195; moving tracks 62
- species `predator` (channels ['predator b'], own threshold): components final 33, mean 24.7, max 37; tracks 128, persistent 6; splits 11, persistent splits 5 (K=20), max generation 1, merges 0, merge/split 0; moving tracks 49
- species `predator_e` (channels ['predator e'], own threshold): components final 12, mean 9.2, max 17; tracks 68, persistent 0; splits 1, persistent splits 0 (K=20), max generation 0, merges 0, merge/split 0; moving tracks 14

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 258 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
