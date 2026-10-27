# Evidence pack: digestion-predators-competition (seed 1)

- world: `../../world2p.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 101 frames x 500 steps x dt 0.2 = time 10000; grid [128, 128]; wall 451s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0457-c52-predator-competition-taxis/world2p.py --out collective/contrib/20261027T0457-c52-predator-competition-taxis/comp/notaxE_s1 --seeds 1 --size 128 128 --frames 100 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1513, 1.8327], min area 6 px

## Measurements
- components: final 34, mean 35.8, max 49; occupancy final 0.21
- tracks: 118; persistent (alive >= 50% of run): 17; longest 99 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 112.00 (1 = constant size)
- enclosures: components with a hole mean 0.39, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 30, 23], H1 [1, 1, 0]
- motion: 49 long-lived tracks moved >= 1 body length; max speed 0.00723/time; max body lengths 7.0
- replication (lineage window K = 20 frames = time 2000, default): splits 31, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 3, merges 9, merge/split ratio 0.29, nucleations 47
- channel total drift (end/start - 1): [-0.029, None, -0.6007, -0.6019, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 51: holes 0, rim-vs-core 0.53, rim-vs-outside 0.18, heterogeneity 0.19; core [0.477, 0.466, 0.234, 0.551, 0.403, 0.323, 0.093] rim [0.317, 0.13, 0.259, 0.362, 0.088, 0.321, 0.06]
  - track 2 at frame 52: holes 0, rim-vs-core 0.53, rim-vs-outside 0.14, heterogeneity 0.18; core [0.39, 0.548, 0.24, 0.439, 0.413, 0.432, 0.128] rim [0.311, 0.149, 0.256, 0.34, 0.085, 0.424, 0.099]
  - track 3 at frame 52: holes 0, rim-vs-core 0.53, rim-vs-outside 0.16, heterogeneity 0.18; core [0.42, 0.524, 0.267, 0.501, 0.408, 0.427, 0.122] rim [0.294, 0.157, 0.289, 0.346, 0.085, 0.42, 0.081]
  - track 90 at frame 87: holes 0, rim-vs-core 0.48, rim-vs-outside 0.19, heterogeneity 0.20; core [0.408, 0.498, 0.275, 0.492, 0.354, 0.454, 0.152] rim [0.309, 0.149, 0.294, 0.373, 0.073, 0.443, 0.109]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 221 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.964, rim/outside 5.2 (aggregate of 221 individuals; 26/221 membrane-like individually; rim level 0.49)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.326, rim/outside 6.97 (aggregate of 221 individuals; 1/221 membrane-like individually; rim level 0.181)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.42, rim/outside 0.882 (aggregate of 221 individuals; 0/221 membrane-like individually; rim level 0.263)
  - radial product p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.95, rim/outside 5.08 (aggregate of 221 individuals; 25/221 membrane-like individually; rim level 0.505)
  - radial digestion q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.272, rim/outside 10.3 (aggregate of 221 individuals; 5/221 membrane-like individually; rim level 0.115)
  - radial predator e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.962, rim/outside 1.07 (aggregate of 221 individuals; 0/221 membrane-like individually; rim level 0.442)
  - radial digestion q2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.917, rim/outside 4 (aggregate of 221 individuals; 21/221 membrane-like individually; rim level 0.189)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=5100, R_eq 4.37): none; #2 (t=5200, R_eq 4.3): none; #3 (t=5200, R_eq 4.18): none; #90 (t=8700, R_eq 4.44): none
- species `prey` (channels ['prey a'], own threshold): components final 28, mean 35.1, max 47; tracks 128, persistent 17; splits 35, persistent splits 16 (K=20), max generation 3, merges 3, merge/split 0.086; moving tracks 52
- species `predator` (channels ['predator b'], own threshold): components final 25, mean 24.8, max 43; tracks 100, persistent 12; splits 12, persistent splits 5 (K=20), max generation 1, merges 1, merge/split 0.083; moving tracks 49
- species `predator_e` (channels ['predator e'], own threshold): components final 1, mean 1.2, max 6; tracks 21, persistent 0; splits 2, persistent splits 0 (K=20), max generation 0, merges 7, merge/split 3.5; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 221 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
