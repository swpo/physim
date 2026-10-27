# Evidence pack: digestion-driven-predators (seed 0)

- world: `../../wconv.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 427s; status ok
- command: `python -m labkit.run c56work/wconv.py --out c56work/cv/A3 --seeds 0 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.26 of robust range [0.156, 1.4946], min area 6 px

## Measurements
- components: final 38, mean 38.7, max 56; occupancy final 0.25
- tracks: 241; persistent (alive >= 50% of run): 0; longest 53 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.17, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [41, 37, 24], H1 [1, 1, 0]
- motion: 17 long-lived tracks moved >= 1 body length; max speed 0.00522/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 2000, default): splits 57, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 10, merge/split ratio 0.175, nucleations 116
- channel total drift (end/start - 1): [-0.0381, None, -0.6071, -0.61, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 29: holes 0, rim-vs-core 0.46, rim-vs-outside 0.26, heterogeneity 0.11; core [0.093, 0.776, 0.275, 0.099, 0.173, 0.71] rim [0.183, 0.347, 0.256, 0.19, 0.068, 0.697]
  - track 0 at frame 27: holes 0, rim-vs-core 0.49, rim-vs-outside 0.26, heterogeneity 0.13; core [0.133, 0.79, 0.261, 0.144, 0.221, 0.589] rim [0.212, 0.331, 0.25, 0.22, 0.078, 0.576]
  - track 10 at frame 29: holes 0, rim-vs-core 0.48, rim-vs-outside 0.12, heterogeneity 0.12; core [0.123, 0.676, 0.255, 0.124, 0.157, 0.726] rim [0.229, 0.239, 0.233, 0.232, 0.048, 0.721]
  - track 187 at frame 106: holes 0, rim-vs-core 0.53, rim-vs-outside 0.17, heterogeneity 0.10; core [0.129, 0.787, 0.334, 0.156, 0.259, 0.666] rim [0.15, 0.287, 0.332, 0.173, 0.078, 0.677]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 234 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.957, rim/outside 4.08 (aggregate of 234 individuals; 29/234 membrane-like individually; rim level 0.436)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.639, rim/outside 6.87 (aggregate of 234 individuals; 2/234 membrane-like individually; rim level 0.348)
  - radial fuel F: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.3, rim/outside 0.907 (aggregate of 234 individuals; 0/234 membrane-like individually; rim level 0.246)
  - radial product p: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.97, rim/outside 3.84 (aggregate of 234 individuals; 29/234 membrane-like individually; rim level 0.436)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.557, rim/outside 8.11 (aggregate of 234 individuals; 12/234 membrane-like individually; rim level 0.121)
  - radial soluble predator u: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 0.993 (aggregate of 234 individuals; 0/234 membrane-like individually; rim level 0.588)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=2900, R_eq 6.05): none; #0 (t=2700, R_eq 6.68): none; #10 (t=2900, R_eq 5.35): none; #187 (t=10600, R_eq 5.61): none
- species `prey` (channels ['prey a'], own threshold): components final 26, mean 31.3, max 46; tracks 271, persistent 0; splits 67, persistent splits 3 (K=20), max generation 1, merges 1, merge/split 0.015; moving tracks 33
- species `predator` (channels ['predator b'], own threshold): components final 30, mean 25.9, max 40; tracks 226, persistent 0; splits 49, persistent splits 4 (K=20), max generation 2, merges 4, merge/split 0.082; moving tracks 30

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 234 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
