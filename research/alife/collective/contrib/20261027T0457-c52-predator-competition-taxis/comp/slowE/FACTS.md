# Evidence pack: digestion-predators-competition (seed 0)

- world: `../../world2p.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 101 frames x 500 steps x dt 0.2 = time 10000; grid [128, 128]; wall 492s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0457-c52-predator-competition-taxis/world2p.py --out collective/contrib/20261027T0457-c52-predator-competition-taxis/comp/slowE --seeds 0 --size 128 128 --frames 100 --no-movie`
- segmentation: matter > 0.16 of robust range [0.152, 2.3083], min area 6 px

## Measurements
- components: final 50, mean 41.3, max 50; occupancy final 0.20
- tracks: 168; persistent (alive >= 50% of run): 19; longest 97 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 24.83 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [46, 42, 33], H1 [0, 0, 0]
- motion: 58 long-lived tracks moved >= 1 body length; max speed 0.00683/time; max body lengths 5.0
- replication (lineage window K = 20 frames = time 2000, default): splits 41, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 2, merges 21, merge/split ratio 0.512, nucleations 65
- channel total drift (end/start - 1): [-0.0436, None, -0.6182, -0.6029, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 17 at frame 52: holes 0, rim-vs-core 0.55, rim-vs-outside 0.21, heterogeneity 0.18; core [0.303, 0.183, 0.211, 0.345, 0.022, 0.58, 0.46] rim [0.321, 0.107, 0.211, 0.356, 0.011, 0.136, 0.151]
  - track 20 at frame 53: holes 0, rim-vs-core 0.06, rim-vs-outside 0.08, heterogeneity 0.09; core [0.296, 0.026, 0.198, 0.316, 0.001, 0.206, 0.021] rim [0.301, 0.023, 0.197, 0.322, 0.001, 0.149, 0.014]
  - track 4 at frame 42: holes 0, rim-vs-core 0.47, rim-vs-outside 0.26, heterogeneity 0.19; core [0.456, 0.459, 0.151, 0.498, 0.469, 0.118, 0.021] rim [0.268, 0.268, 0.189, 0.287, 0.149, 0.093, 0.007]
  - track 118 at frame 87: holes 0, rim-vs-core 0.56, rim-vs-outside 0.16, heterogeneity 0.25; core [0.417, 0.489, 0.171, 0.466, 0.308, 0.23, 0.359] rim [0.31, 0.183, 0.19, 0.338, 0.075, 0.0, 0.066]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 265 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.984, rim/outside 3.46 (aggregate of 265 individuals; 30/265 membrane-like individually; rim level 0.439)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.406, rim/outside 5.47 (aggregate of 265 individuals; 5/265 membrane-like individually; rim level 0.147)
  - radial fuel F: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.34, rim/outside 0.881 (aggregate of 265 individuals; 0/265 membrane-like individually; rim level 0.199)
  - radial product p: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.968, rim/outside 3.5 (aggregate of 265 individuals; 21/265 membrane-like individually; rim level 0.456)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.355, rim/outside 8.42 (aggregate of 265 individuals; 9/265 membrane-like individually; rim level 0.0917)
  - radial predator e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.405, rim/outside 7.01 (aggregate of 265 individuals; 4/265 membrane-like individually; rim level 0.159)
  - radial digestion q2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.399, rim/outside 9.17 (aggregate of 265 individuals; 9/265 membrane-like individually; rim level 0.0966)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #17 (t=5200, R_eq 4.48): none; #20 (t=5300, R_eq 3.52): none; #4 (t=4200, R_eq 5.14): none; #118 (t=8700, R_eq 4.55): none
- species `prey` (channels ['prey a'], own threshold): components final 42, mean 38.6, max 49; tracks 173, persistent 14; splits 36, persistent splits 10 (K=20), max generation 2, merges 3, merge/split 0.083; moving tracks 62
- species `predator` (channels ['predator b'], own threshold): components final 25, mean 17.8, max 31; tracks 124, persistent 0; splits 8, persistent splits 1 (K=20), max generation 1, merges 0, merge/split 0; moving tracks 34
- species `predator_e` (channels ['predator e'], own threshold): components final 22, mean 17.9, max 28; tracks 121, persistent 1; splits 2, persistent splits 0 (K=20), max generation 0, merges 0, merge/split 0; moving tracks 33

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 265 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
